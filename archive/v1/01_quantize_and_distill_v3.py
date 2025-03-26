#!/usr/bin/env python

import os
import json
import torch
import random
from torch import nn
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset
import numpy as np

from sentence_transformers import SentenceTransformer, models
from transformers import AutoModel, BertConfig

########################################################
# CONFIG
########################################################
TEACHER_MODEL_NAME = "intfloat/multilingual-e5-small"
STUDENT_NUM_LAYERS = 3
STUDENT_NUM_HEADS = 8
STUDENT_HIDDEN_SIZE = 384  # multiple of HEADS
STUDENT_INTERMEDIATE_SIZE = 1024

# Path to your icons JSON with each icon having "name" & "tags"
ICONS_JSON_FILE = "../../data/icons.json"

# Distilled outputs
STUDENT_DIR = "../distilled_domain_model"
ONNX_PATH = "../../domain_model.onnx"
ONNX_QUANT_PATH = "../../domain_model_quant.onnx"

# Training
MAX_SEQ_LEN = 128
EPOCHS = 20
BATCH_SIZE = 16
LR = 1e-4

########################################################
# 1) TEACHER
########################################################
teacher = SentenceTransformer(TEACHER_MODEL_NAME, device="cpu")
teacher.eval()
for p in teacher.parameters():
    p.requires_grad = False

teacher_dim = teacher.get_sentence_embedding_dimension()

########################################################
# 2) STUDENT CONFIG
########################################################
teacher_cfg = teacher[0].auto_model.config
teacher_dict = teacher_cfg.to_dict()

teacher_dict["num_hidden_layers"] = STUDENT_NUM_LAYERS
teacher_dict["num_attention_heads"] = STUDENT_NUM_HEADS
teacher_dict["hidden_size"] = STUDENT_HIDDEN_SIZE
teacher_dict["intermediate_size"] = STUDENT_INTERMEDIATE_SIZE
student_cfg = BertConfig(**teacher_dict)

########################################################
# 3) BUILD STUDENT
########################################################
hf_student = AutoModel.from_config(student_cfg)
transformer_module = models.Transformer(
    model_name_or_path=TEACHER_MODEL_NAME,  # same tokenizer
    max_seq_length=MAX_SEQ_LEN
)
transformer_module.auto_model = hf_student
pooling_module = models.Pooling(STUDENT_HIDDEN_SIZE, pooling_mode="mean")

student = SentenceTransformer(modules=[transformer_module, pooling_module], device="cpu")
student_dim = student.get_sentence_embedding_dimension()

########################################################
# 4) ICON TAGS => TRAINING DATA
########################################################
# We'll gather all icon tags as text lines. The teacher sees them, the student sees them,
# then we do MSE on the resulting embeddings. This forcibly keeps "cat" knowledge.

with open(ICONS_JSON_FILE, "r", encoding="utf-8") as f:
    icons_data = json.load(f)
icons = icons_data["icons"]

# Gather texts from each icon. E.g. name + tags
all_texts = []
for icon in icons:
    text = icon["name"] + " " + icon["tags"]
    all_texts.append(text)

# Deduplicate
all_texts = list(set(all_texts))

class DomainDataset(Dataset):
    def __init__(self, texts):
        self.texts = texts
    def __len__(self):
        return len(self.texts)
    def __getitem__(self, idx):
        return self.texts[idx]

ds = DomainDataset(all_texts)

# We'll tokenize using teacher's tokenizer
def collate_fn(batch):
    return teacher.tokenizer(
        batch,
        padding="longest",
        truncation=True,
        max_length=MAX_SEQ_LEN,
        return_tensors="pt"
    )

dl = DataLoader(ds, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)

########################################################
# 5) DIM MISMATCH? TEACHER=384, STUDENT=256
# We add a small linear layer to map teacher-emb => student-dim
########################################################
teacher_squisher = nn.Linear(teacher_dim, student_dim, bias=False)
teacher_squisher.to("cpu")

# We'll optimize both student + squisher
params = list(student.parameters()) + list(teacher_squisher.parameters())
optimizer = AdamW(params, lr=LR)
criterion = nn.MSELoss()

########################################################
# 6) TRAINING
########################################################
student.train()
print("=== Domain Distillation Training ===")
for epoch in range(EPOCHS):
    total_loss = 0.0
    for batch in dl:
        with torch.no_grad():
            teacher_out = teacher({"input_ids": batch["input_ids"], "attention_mask": batch["attention_mask"]})
            teacher_emb = teacher_out["sentence_embedding"]  # shape [B, teacher_dim]

        student_out = student({"input_ids": batch["input_ids"], "attention_mask": batch["attention_mask"]})
        student_emb = student_out["sentence_embedding"]      # shape [B, student_dim]

        # Map teacher emb -> student dim
        teacher_slim = teacher_squisher(teacher_emb)

        loss = criterion(student_emb, teacher_slim)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    avg_loss = total_loss / len(dl)
    print(f"Epoch {epoch+1}/{EPOCHS} loss={avg_loss:.4f}")

########################################################
# 7) SAVE
########################################################
student.save(STUDENT_DIR)
torch.save(teacher_squisher.state_dict(), os.path.join(STUDENT_DIR, "teacher_squisher.pt"))
print(f"Student & squisher saved to {STUDENT_DIR}")

########################################################
# 8) EXPORT ONNX
########################################################
import torch.onnx

class ONNXWrapper(torch.nn.Module):
    def __init__(self, st_model, squish):
        super().__init__()
        self.st_model = st_model
        self.squish = squish

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.st_model({"input_ids": input_ids, "attention_mask": attention_mask})
            student_emb = out["sentence_embedding"]  # [B, student_dim]
            # Optionally, if you want the same dimension as teacher,
            # you can invert it. For now, we just keep the student dim
            return student_emb

def export_onnx(st_dir, onnx_path):
    print(f"Loading student from: {st_dir}")
    st_model = SentenceTransformer(st_dir, device="cpu")
    st_model.eval()

    # If you want to incorporate teacher_squisher in the final output,
    # load it and do wrapper. Right now we skip that => output is 256-dim
    squish = nn.Linear(teacher_dim, student_dim, bias=False)
    squisher_path = os.path.join(st_dir, "teacher_squisher.pt")
    if os.path.exists(squisher_path):
        squish.load_state_dict(torch.load(squisher_path))

    wrapper = ONNXWrapper(st_model, squish).eval()

    dummy_input_ids = torch.randint(0, 1000, (1, 128), dtype=torch.long)
    dummy_attention_mask = torch.ones((1, 128), dtype=torch.long)

    print(f"Exporting ONNX => {onnx_path}")
    torch.onnx.export(
        wrapper,
        (dummy_input_ids, dummy_attention_mask),
        onnx_path,
        input_names=["input_ids", "attention_mask"],
        output_names=["output"],
        opset_version=14,
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "attention_mask": {0: "batch_size", 1: "sequence_length"},
            "output": {0: "batch_size"}
        }
    )
    print("Export complete.")

export_onnx(STUDENT_DIR, ONNX_PATH)

########################################################
# 9) QUANTIZE
########################################################
from onnxruntime.quantization import quantize_dynamic, QuantType
def quantize_onnx(in_path, out_path):
    print(f"Quantizing {in_path} => {out_path}")
    quantize_dynamic(
        model_input=in_path,
        model_output=out_path,
        per_channel=False,
        reduce_range=False,
        weight_type=QuantType.QUInt8
    )
    size_mb = os.path.getsize(out_path)/(1024*1024)
    print(f"Quantized => {out_path}  (~{size_mb:.1f} MB)")

quantize_onnx(ONNX_PATH, ONNX_QUANT_PATH)
print("Done.")

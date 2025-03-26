#!/usr/bin/env python

import os
import torch
import random
import numpy as np

from torch import nn
from torch.optim import AdamW
from torch.utils.data import DataLoader, Dataset

# For quantization
from onnxruntime.quantization import quantize_dynamic, QuantType

# Sentence-Transformers & Transformers
from sentence_transformers import SentenceTransformer, models
from transformers import AutoModel, BertConfig

########################################
# CONFIG
########################################
TEACHER_MODEL_NAME = "intfloat/multilingual-e5-small"
# The teacher often outputs 384-dim embeddings (E5-Small).
# We'll build a smaller student, e.g. 256-dim

STUDENT_NUM_LAYERS = 3
STUDENT_NUM_HEADS = 8
STUDENT_HIDDEN_SIZE = 256
STUDENT_INTERMEDIATE_SIZE = 1024
MAX_SEQ_LENGTH = 128
NUM_EPOCHS = 1
BATCH_SIZE = 8
LEARNING_RATE = 1e-4

STUDENT_SAVE_FOLDER = "distilled_e5_student"
ONNX_PATH = "../../distilled_e5_student.onnx"
ONNX_QUANT_PATH = "../../distilled_e5_student_quant.onnx"


########################################
# 1) TEACHER MODEL
########################################
print(f"Loading teacher: {TEACHER_MODEL_NAME}")
teacher_model = SentenceTransformer(TEACHER_MODEL_NAME, device="cpu")
teacher_model.eval()
for p in teacher_model.parameters():
    p.requires_grad = False

teacher_tokenizer = teacher_model.tokenizer

# Let’s see the teacher embedding dimension
teacher_dim = teacher_model.get_sentence_embedding_dimension()
print(f"Teacher embedding dim = {teacher_dim}")

# We'll read teacher config so we can copy it
teacher_config = teacher_model[0].auto_model.config
teacher_dict = teacher_config.to_dict()

########################################
# 2) STUDENT CONFIG
########################################
teacher_dict["num_hidden_layers"] = STUDENT_NUM_LAYERS
teacher_dict["num_attention_heads"] = STUDENT_NUM_HEADS
teacher_dict["hidden_size"] = STUDENT_HIDDEN_SIZE
teacher_dict["intermediate_size"] = STUDENT_INTERMEDIATE_SIZE
student_cfg = BertConfig(**teacher_dict)

########################################
# 3) BUILD STUDENT
########################################
huggingface_student = AutoModel.from_config(student_cfg)

transformer_module = models.Transformer(
    model_name_or_path=TEACHER_MODEL_NAME,  # same tokenizer
    max_seq_length=MAX_SEQ_LENGTH
)
transformer_module.auto_model = huggingface_student
pooling_module = models.Pooling(student_cfg.hidden_size, pooling_mode="mean")

student_model = SentenceTransformer(
    modules=[transformer_module, pooling_module],
    device="cpu"
)
student_model.train()

# Student embedding dim
student_dim = student_model.get_sentence_embedding_dimension()
print(f"Student embedding dim = {student_dim}")

# 4) The squisher: teacher_emb (384) -> student_emb (256)
#    We'll train this linear layer so we can do MSE in the same dimension.
teacher_squisher = nn.Linear(teacher_dim, student_dim, bias=False).to("cpu")

########################################
# 5) SAMPLE TRAIN DATA
########################################
train_texts = [
    "Hello world",
    "Text for distillation",
    "Пример на русском",
    "Bonjour, un exemple en français",
    "Hola, un ejemplo en español",
] * 10

class DistillDataset(Dataset):
    def __init__(self, texts):
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx]

def collate_fn(batch):
    enc = teacher_tokenizer(
        batch,
        padding="longest",
        truncation=True,
        max_length=MAX_SEQ_LENGTH,
        return_tensors="pt"
    )
    return enc

dataset = DistillDataset(train_texts)
dataloader = DataLoader(
    dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn
)

########################################
# 6) TRAINING (DISTILLATION)
########################################
# We'll optimize BOTH the student and the teacher_squisher
all_params = list(student_model.parameters()) + list(teacher_squisher.parameters())
optimizer = AdamW(all_params, lr=LEARNING_RATE)
criterion = nn.MSELoss()

print("\n=== Distillation Training ===")
for epoch in range(NUM_EPOCHS):
    total_loss = 0.0
    for batch_data in dataloader:
        with torch.no_grad():
            teacher_out = teacher_model({
                "input_ids": batch_data["input_ids"],
                "attention_mask": batch_data["attention_mask"]
            })
            teacher_emb = teacher_out["sentence_embedding"]  # shape [B, teacher_dim]

        student_out = student_model({
            "input_ids": batch_data["input_ids"],
            "attention_mask": batch_data["attention_mask"]
        })
        student_emb = student_out["sentence_embedding"]      # shape [B, student_dim]

        # We do teacher_slim = teacher_squisher(teacher_emb)
        teacher_slim = teacher_squisher(teacher_emb)         # shape [B, student_dim]

        # Now MSE
        loss = criterion(student_emb, teacher_slim)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{NUM_EPOCHS}, loss={avg_loss:.4f}")

# Save final student
student_model.save(STUDENT_SAVE_FOLDER)
# We'll also save teacher_squisher separately
torch.save(teacher_squisher.state_dict(), os.path.join(STUDENT_SAVE_FOLDER, "teacher_squisher.pt"))
print(f"\nStudent saved to: {STUDENT_SAVE_FOLDER}")

########################################
# 7) EXPORT STUDENT TO ONNX
########################################
# The user might also want to incorporate teacher_squisher at inference time
# if you want the student to produce exactly the "teacher-like" dimension.
# But if your app uses the student's final (256-dim) embeddings, you don't need the squisher at inference.
import torch.onnx

class ONNXWrapper(torch.nn.Module):
    def __init__(self, st_model):
        super().__init__()
        self.st_model = st_model

    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            out = self.st_model({
                "input_ids": input_ids,
                "attention_mask": attention_mask
            })
            # This returns the student's 256-dim embeddings
            # If you want 384-dim "teacher-like" embeddings, you'd incorporate the teacher_squisher
            return out["sentence_embedding"]

def export_to_onnx(model_dir, onnx_path, seq_len=128):
    print(f"\nLoading student from {model_dir}")
    st_model = SentenceTransformer(model_dir, device="cpu")
    st_model.eval()

    wrapper = ONNXWrapper(st_model).eval()
    dummy_input_ids = torch.randint(0, 1000, (1, seq_len), dtype=torch.long)
    dummy_attention_mask = torch.ones((1, seq_len), dtype=torch.long)

    print("Exporting ONNX…")
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
    print(f"ONNX exported to {onnx_path}")

export_to_onnx(STUDENT_SAVE_FOLDER, ONNX_PATH, seq_len=MAX_SEQ_LENGTH)

########################################
# 8) QUANTIZE
########################################
def quantize_onnx(input_path, output_path):
    print(f"\nQuantizing {input_path} => {output_path}")
    quantize_dynamic(
        model_input=input_path,
        model_output=output_path,
        per_channel=False,
        reduce_range=False,
        weight_type=QuantType.QUInt8
    )
    size_mb = os.path.getsize(output_path) / (1024*1024)
    print(f"Quantized size: {size_mb:.1f} MB")

quantize_onnx(ONNX_PATH, ONNX_QUANT_PATH)
print("\nAll done!\n")

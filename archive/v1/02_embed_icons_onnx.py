#!/usr/bin/env python

import os
import json
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

# CONFIG
ONNX_MODEL_PATH = "../../distilled_e5_student_quant.onnx"  # your quantized ONNX
TOKENIZER_NAME = "intfloat/multilingual-e5-small"    # or your choice
ICONS_JSON_FILE = "../../data/icons.json"
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"
MAX_SEQ_LENGTH = 128

# 1) Setup ONNX + Tokenizer
print(f"Loading ONNX model: {ONNX_MODEL_PATH}")
session = ort.InferenceSession(ONNX_MODEL_PATH, providers=["CPUExecutionProvider"])

print(f"Loading tokenizer: {TOKENIZER_NAME}")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

# 2) Embed icons
def embed_icons():
    with open(ICONS_JSON_FILE, "r", encoding="utf-8") as f:
        icons_data = json.load(f)
    icons = icons_data["icons"]
    print(f"Found {len(icons)} icons")

    all_embeddings = []
    metadata = []

    for icon in icons:
        text = icon["name"] + " " + icon["tags"]
        # Tokenize
        inputs = tokenizer(text, return_tensors="np", padding="max_length",
                           max_length=MAX_SEQ_LENGTH, truncation=True)

        # Run ONNX
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
        }
        outputs = session.run(None, ort_inputs)
        emb = outputs[0].flatten()  # shape: (embedding_dim,)

        all_embeddings.append(emb)
        metadata.append({"id": icon["name"], "tags": icon["tags"]})

    # Save
    all_embeddings = np.array(all_embeddings)
    np.save(ICON_EMBEDS_NPY, all_embeddings)
    with open(ICON_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Embeddings saved: {ICON_EMBEDS_NPY}")
    print(f"Metadata saved: {ICON_INDEX_JSON}")

if __name__ == "__main__":
    embed_icons()

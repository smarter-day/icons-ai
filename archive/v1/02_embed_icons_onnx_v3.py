#!/usr/bin/env python

import os
import json
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
ONNX_MODEL = "domain_model_quant.onnx"        # Your ~63.7 MB distilled & quantized model
TOKENIZER_NAME = "intfloat/multilingual-e5-small"  # Same as teacher
ICONS_JSON = "data/icons.json"
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"
MAX_SEQ_LENGTH = 128

# -----------------------------------------------------------------------------
# 1) Setup ONNX + Tokenizer
# -----------------------------------------------------------------------------
print(f"Loading ONNX model: {ONNX_MODEL}")
session = ort.InferenceSession(ONNX_MODEL, providers=["CPUExecutionProvider"])

print(f"Loading tokenizer: {TOKENIZER_NAME}")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

# -----------------------------------------------------------------------------
# 2) Embed Icons
# -----------------------------------------------------------------------------
def embed_icons():
    with open(ICONS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    icons = data["icons"]
    print(f"Found {len(icons)} icons in {ICONS_JSON}")

    all_embs = []
    meta = []

    for icon in icons:
        text = icon["name"] + " " + icon["tags"]
        # Tokenize
        inputs = tokenizer(text, return_tensors="np",
                           max_length=MAX_SEQ_LENGTH, truncation=True, padding="max_length")
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64)
        }
        # Run ONNX
        outputs = session.run(None, ort_inputs)  # returns a tuple (embedding,)
        emb = outputs[0].flatten()               # shape (embedding_dim,)

        all_embs.append(emb)
        meta.append({"id": icon["name"], "tags": icon["tags"]})

    all_embs = np.array(all_embs)
    np.save(ICON_EMBEDS_NPY, all_embs)
    print(f"Icon embeddings => {ICON_EMBEDS_NPY}")

    with open(ICON_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Icon metadata => {ICON_INDEX_JSON}")

if __name__ == "__main__":
    embed_icons()

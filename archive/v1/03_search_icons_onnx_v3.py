#!/usr/bin/env python

import os
import json
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from scipy.spatial.distance import cosine

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
ONNX_MODEL = "domain_model_quant.onnx"
TOKENIZER_NAME = "intfloat/multilingual-e5-small"
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
# 2) Search
# -----------------------------------------------------------------------------
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="np",
                       max_length=MAX_SEQ_LENGTH, truncation=True, padding="max_length")
    ort_inputs = {
        "input_ids": inputs["input_ids"].astype(np.int64),
        "attention_mask": inputs["attention_mask"].astype(np.int64)
    }
    outputs = session.run(None, ort_inputs)
    return outputs[0].flatten()

def search_icons(query, top_k=5):
    # Load precomputed icons
    icon_embs = np.load(ICON_EMBEDS_NPY)
    with open(ICON_INDEX_JSON, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Query -> embedding
    q_emb = get_embedding(query)

    # Compute similarities
    sims = []
    for emb in icon_embs:
        sim = 1 - cosine(q_emb, emb)
        sims.append(sim)

    # Top-k
    sims = np.array(sims)
    top_idx = np.argsort(sims)[::-1][:top_k]

    results = []
    for i in top_idx:
        results.append({
            "icon_id": meta[i]["id"],
            "tags": meta[i]["tags"],
            "similarity": float(sims[i])
        })
    return results

def main():
    query = input("Enter query: ")
    top_res = search_icons(query)
    for r in top_res:
        print(f"[{r['similarity']:.3f}]  ID={r['icon_id']} | tags={r['tags']}")

if __name__ == "__main__":
    main()

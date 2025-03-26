#!/usr/bin/env python

import os
import json
import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer
from scipy.spatial.distance import cosine

# CONFIG
ONNX_MODEL_PATH = "../../distilled_e5_student_quant.onnx"
TOKENIZER_NAME = "intfloat/multilingual-e5-small"
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"
MAX_SEQ_LENGTH = 128

# 1) Setup ONNX + Tokenizer
print(f"Loading ONNX model: {ONNX_MODEL_PATH}")
session = ort.InferenceSession(ONNX_MODEL_PATH, providers=["CPUExecutionProvider"])

print(f"Loading tokenizer: {TOKENIZER_NAME}")
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME)

# 2) Search function
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="np", padding="max_length",
                       max_length=MAX_SEQ_LENGTH, truncation=True)
    ort_inputs = {
        "input_ids": inputs["input_ids"].astype(np.int64),
        "attention_mask": inputs["attention_mask"].astype(np.int64),
    }
    outputs = session.run(None, ort_inputs)
    return outputs[0].flatten()

def search_icons(query, top_k=5):
    # Load icon embeddings + metadata
    icon_embeds = np.load(ICON_EMBEDS_NPY)
    with open(ICON_INDEX_JSON, "r", encoding="utf-8") as f:
        icon_meta = json.load(f)

    # Embed query
    query_emb = get_embedding(query)

    # Cosine similarity to each icon
    similarities = []
    for icon_emb in icon_embeds:
        sim = 1 - cosine(query_emb, icon_emb)
        similarities.append(sim)

    # Top K
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = []
    for i in top_indices:
        results.append({
            "icon_id": icon_meta[i]["id"],
            "tags": icon_meta[i]["tags"],
            "similarity": float(similarities[i])
        })
    return results

def main():
    query = input("Enter query: ")
    results = search_icons(query)
    for r in results:
        print(f"[{r['similarity']:.3f}]  ID={r['icon_id']}, tags={r['tags']}")

if __name__ == "__main__":
    main()

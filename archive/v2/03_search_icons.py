#!/usr/bin/env python
import os
import json
import numpy as np
import fasttext
from scipy.spatial.distance import cosine

FINAL_MODEL = "icons_ft.bin"
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"

def embed_text(ft_model, text):
    tokens = text.strip().split()
    tokens = [t for t in tokens if not t.startswith("__label__")]
    if not tokens:
        return np.zeros(ft_model.get_dimension())
    return np.mean([ft_model.get_word_vector(t) for t in tokens], axis=0)

def search_icons(query, top_k=5):
    # Load
    ft_model = fasttext.load_model(FINAL_MODEL)
    icon_embs = np.load(ICON_EMBEDS_NPY)
    with open(ICON_INDEX_JSON, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Embed
    q_emb = embed_text(ft_model, query)

    # Compute similarity
    sims = []
    for i, emb in enumerate(icon_embs):
        s = 1 - cosine(q_emb, emb)
        sims.append((s, meta[i]))

    # Sort + return
    sims.sort(key=lambda x: x[0], reverse=True)
    return sims[:top_k]

def main():
    while True:
        q = input("Enter query: ").strip()
        if not q:
            break
        results = search_icons(q)
        for sim, meta in results:
            print(f"[{sim:.3f}] ID={meta['id']}  tags={meta['tags']}")

if __name__ == "__main__":
    main()

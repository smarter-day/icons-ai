#!/usr/bin/env python

import os
import json
import math

ICON_EMBEDDINGS_JSON = "embeddings/icon_embeddings.ru.json"
WORD_EMBEDDINGS_JSON = "embeddings/vocab_embeddings.ru.json"

def load_json_embeddings():
    if not os.path.exists(ICON_EMBEDDINGS_JSON):
        raise FileNotFoundError(f"Missing {ICON_EMBEDDINGS_JSON}")
    if not os.path.exists(WORD_EMBEDDINGS_JSON):
        raise FileNotFoundError(f"Missing {WORD_EMBEDDINGS_JSON}")

    with open(ICON_EMBEDDINGS_JSON, "r", encoding="utf-8") as f:
        icon_embeds = json.load(f)
    with open(WORD_EMBEDDINGS_JSON, "r", encoding="utf-8") as f:
        vocab_embeds = json.load(f)

    return icon_embeds, vocab_embeds

def average_embedding(text: str, vocab: dict):
    """
    - Tokenize text
    - For each token, look up vocab[token.lower()]
    - Average them
    - Return list of floats
    """
    tokens = text.lower().replace(",", " ").split()
    vecs = []
    for t in tokens:
        if t in vocab:
            vecs.append(vocab[t])
    if not vecs:
        return None  # or a zero vector
    # average
    # "vecs" is a list of lists. We can sum up dimension-wise and then divide
    dim = len(vecs[0])
    sums = [0.0]*dim
    for v in vecs:
        for i in range(dim):
            sums[i] += v[i]
    count = len(vecs)
    return [val/count for val in sums]

def cosine_similarity(v1, v2):
    """
    v1, v2 are lists of floats
    """
    if len(v1) != len(v2):
        return 0.0
    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0
    for a, b in zip(v1, v2):
        dot += a*b
        norm1 += a*a
        norm2 += b*b
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (math.sqrt(norm1)*math.sqrt(norm2))

def search_icons(query, top_k=5):
    """
    1) Embed query from words
    2) Compare to icon embeddings by cos sim
    3) Return top_k
    """
    icon_embeds, vocab_embeds = load_json_embeddings()
    query_vec = average_embedding(query, vocab_embeds)
    if query_vec is None:
        return []  # no known words in query

    # Compare
    results = []
    for icon_id, icon_vec in icon_embeds.items():
        sim = cosine_similarity(query_vec, icon_vec)
        results.append((icon_id, sim))

    # Sort desc by similarity
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]

def main():
    while True:
        user_input = input("\nEnter search query (or blank to quit): ")
        user_input = user_input.strip()
        if not user_input:
            break
        top_results = search_icons(user_input)
        for icon_id, sim in top_results:
            print(f"[{sim:.3f}]  {icon_id}")

if __name__ == "__main__":
    main()

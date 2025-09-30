#!/usr/bin/env python

import os
import json
import fasttext
import numpy as np
from collections import defaultdict

# -------------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------------
FASTTEXT_MODEL_PATH = f".models/cc.en.200.bin"
ICONS_JSON_PATH = f"data/icons.stripped.json"
ICON_EMBEDDINGS_JSON = f"embeddings/icon_embeddings.json"
WORD_EMBEDDINGS_JSON = f"embeddings/vocab_embeddings.json"
ROUND_DECIMALS = 2  # Round to 1 decimal places

# -------------------------------------------------------------------------
def load_fasttext_model():
    if not os.path.exists(FASTTEXT_MODEL_PATH):
        raise FileNotFoundError(f"Missing FastText model at: {FASTTEXT_MODEL_PATH}")
    print(f"Loading FastText model: {FASTTEXT_MODEL_PATH}")
    model = fasttext.load_model(FASTTEXT_MODEL_PATH)
    print("Model loaded.")
    return model

def create_icon_embeddings(model):
    with open(ICONS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    icons = data["icons"]
    print(f"Found {len(icons)} icons")

    icon_embeds = {}
    all_words = set()

    for icon in icons:
        text = icon["name"] + " " + icon["tags"]
        tokens = text.replace(",", " ").strip().split()
        tokens = [t.lower() for t in tokens if t.strip()]

        vecs = []
        for word in tokens:
            arr = model.get_word_vector(word)
            vecs.append(arr)
            all_words.add(word)

        if not vecs:
            emb = np.zeros(model.get_dimension(), dtype=np.float32)
        else:
            emb = np.mean(vecs, axis=0)

        # Convert to list and round each float
        emb_list = [round(float(x), ROUND_DECIMALS) for x in emb]
        icon_id = icon["name"]
        icon_embeds[icon_id] = emb_list

    return icon_embeds, all_words

def create_word_vocab_embeddings(model, word_list):
    vocab_dict = {}
    for w in word_list:
        vec = model.get_word_vector(w)
        # Round each float
        vocab_dict[w] = [round(float(x), ROUND_DECIMALS) for x in vec]
    return vocab_dict

def main():
    ft_model = load_fasttext_model()

    icon_embeds, word_set = create_icon_embeddings(ft_model)
    vocab_dict = create_word_vocab_embeddings(ft_model, word_set)

    with open(ICON_EMBEDDINGS_JSON, "w", encoding="utf-8") as f:
        json.dump(icon_embeds, f, ensure_ascii=False)
    print(f"Saved icon embeddings => {ICON_EMBEDDINGS_JSON}")

    with open(WORD_EMBEDDINGS_JSON, "w", encoding="utf-8") as f:
        json.dump(vocab_dict, f, ensure_ascii=False)
    print(f"Saved word embeddings => {WORD_EMBEDDINGS_JSON}")

    print("Done.")

if __name__ == "__main__":
    main()

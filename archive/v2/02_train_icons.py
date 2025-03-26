#!/usr/bin/env python

import os
import json
import fasttext
import numpy as np

##############################################################################
# CONFIG
##############################################################################
DIM = 10          # Must match your base model dimension
LANG = 'en'
BASE_MODEL = f"cc.{LANG}.{DIM}.bin"       # The dimension-reduced file you already have
ICONS_JSON = "data/icons.json"    # Your icons data
SUPERVISED_TXT = "icons_supervised.txt"
FINAL_MODEL = "icons_ft.bin"
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"

EPOCHS = 20
LR = 0.05
CUTOFF = 100000   # For quantize

##############################################################################
# 1) BUILD FAKE SUPERVISED CORPUS
##############################################################################
def build_supervised_corpus():
    """
    Convert your icons into lines with dummy label, e.g.:
    '__label__icons cat kitty meow'
    """
    with open(ICONS_JSON, "r", encoding="utf-8") as f:
        icons_data = json.load(f)
    icons = icons_data["icons"]

    with open(SUPERVISED_TXT, "w", encoding="utf-8") as fout:
        for icon in icons:
            text = icon["name"] + " " + icon["tags"]
            text = text.replace(",", " ")
            fout.write(f"__label__icons {text}\n")

    print(f"Created {SUPERVISED_TXT} with dummy labels.")

##############################################################################
# 2) TRAIN SUPERVISED + QUANTIZE
##############################################################################
def train_and_quantize():
    """
    - Trains a new supervised model from the dummy-labeled file,
    - Then quantizes it to a final .bin
    """
    print(f"Training supervised model using base dimension={DIM}.")
    model = fasttext.train_supervised(
        input=SUPERVISED_TXT,
        lr=LR,
        epoch=EPOCHS,
        dim=DIM,
        label="__label__"  # Our dummy label prefix
    )
    print("Supervised training complete.")

    print("Quantizing the supervised model ...")
    model.quantize(
        input=SUPERVISED_TXT,
        retrain=True,
        cutoff=CUTOFF
    )
    model.save_model(FINAL_MODEL)
    print(f"Final domain model => {FINAL_MODEL}")

    # Clean up
    os.remove(SUPERVISED_TXT)

##############################################################################
# 3) EMBED TEXTS (IGNORE LABELS)
##############################################################################
def embed_text(model: fasttext.FastText._FastText, text: str):
    """
    Averages word vectors for all tokens (ignoring any label tokens).
    """
    tokens = text.replace(",", " ").strip().split()
    tokens = [t for t in tokens if not t.startswith("__label__")]
    if not tokens:
        return np.zeros(model.get_dimension(), dtype=np.float32)

    vecs = [model.get_word_vector(tok) for tok in tokens]
    return np.mean(vecs, axis=0)

##############################################################################
# 4) EMBED ICONS
##############################################################################
def embed_icons():
    model = fasttext.load_model(FINAL_MODEL)
    print(f"Loaded final model => {FINAL_MODEL}")

    with open(ICONS_JSON, "r", encoding="utf-8") as f:
        icons_data = json.load(f)
    icons = icons_data["icons"]

    all_embs = []
    meta = []
    for icon in icons:
        txt = icon["name"] + " " + icon["tags"]
        emb = embed_text(model, txt)
        all_embs.append(emb)
        meta.append({"id": icon["name"], "tags": icon["tags"]})

    all_embs = np.array(all_embs)
    np.save(ICON_EMBEDS_NPY, all_embs)
    with open(ICON_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Saved icon embeddings => {ICON_EMBEDS_NPY}")
    print(f"Saved icon metadata => {ICON_INDEX_JSON}")

##############################################################################
# MAIN
##############################################################################
def main():
    # 1) Ensure your base file cc.en.50.bin is present
    if not os.path.exists(BASE_MODEL):
        raise FileNotFoundError(f"Missing base model {BASE_MODEL}")

    # 2) Build the dummy-labeled corpus
    build_supervised_corpus()

    # 3) Train + quantize (supervised approach)
    train_and_quantize()

    # 4) Embed icons using the final quantized model
    embed_icons()

if __name__ == "__main__":
    main()

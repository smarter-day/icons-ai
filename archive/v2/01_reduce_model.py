#!/usr/bin/env python

import os
import json
import fasttext
import numpy as np

import fasttext.util

###########################################################
# CONFIG
###########################################################
LANGUAGE = "en"
DEFAULT_DIM = 300
SMALL_DIM = 10

FULL_MODEL_NAME_TMPL = "cc.{language}.{dimension}.bin"
DEFAULT_MODEL_NAME = FULL_MODEL_NAME_TMPL.format(
    language=LANGUAGE,
    dimension=DEFAULT_DIM,
)
SMALL_MODEL_NAME = FULL_MODEL_NAME_TMPL.format(
    language=LANGUAGE,
    dimension=SMALL_DIM,
)
SMALL_QUANT_MODEL_NAME = SMALL_MODEL_NAME.replace(".bin", "compact_quantized.bin")

# Where we put the final icons domain model
FINAL_MODEL = "icons_ft.bin"

# Icons JSON
ICONS_JSON_FILE = "data/icons.json"

# Temporary data
SUPERVISED_TXT = "icons_supervised.txt"
TEMP_VECS = "base_vectors.vec"

# Final embeddings
ICON_EMBEDS_NPY = "data/icon_embeddings.npy"
ICON_INDEX_JSON = "data/icons_index.json"

# fastText hyperparams
EPOCHS = 10
LR = 0.05
CUTOFF = 100000

###########################################################
# 1) DOWNLOAD & DIM REDUCE THE BASE FASTTEXT MODEL
###########################################################
def prepare_base_model():
    # 1. Download standard 300‐dim English model if not present
    fasttext.util.download_model(LANGUAGE, if_exists="ignore")
    # => "cc.en.300.bin" if LANGUAGE="en"

    # 2. Load
    print(f"Loading default model: {DEFAULT_MODEL_NAME}")
    model = fasttext.load_model(DEFAULT_MODEL_NAME)

    # 3. Reduce dimension to SMALL_DIM
    print(f"Reducing dimension from {DEFAULT_DIM} => {SMALL_DIM}")
    fasttext.util.reduce_model(model, SMALL_DIM)
    model.save_model(SMALL_MODEL_NAME)

    # 4. (Optional) we do an initial quantize just to keep it small
    # print("Initial quantize of the small model...")
    # model = fasttext.load_model(SMALL_MODEL_NAME)
    # model.quantize(retrain=False, cutoff=CUTOFF)
    # model.save_model(SMALL_QUANT_MODEL_NAME)
    # print(f"Created {SMALL_QUANT_MODEL_NAME} as a small base model.\n")

###########################################################
# 2) BUILD FAKE SUPERVISED CORPUS
###########################################################
def build_supervised_corpus():
    """
    We add a dummy label: '__label__icons ' at the start of each line.
    This allows train_supervised + model.quantize to work in Python.
    """
    with open(ICONS_JSON_FILE, "r", encoding="utf-8") as f:
        icons_data = json.load(f)
    icons = icons_data["icons"]

    with open(SUPERVISED_TXT, "w", encoding="utf-8") as fout:
        for icon in icons:
            # combine name + tags
            line_text = icon["name"] + " " + icon["tags"]
            line_text = line_text.replace(",", " ")
            # e.g. "__label__icons cat cat feline pet"
            fout.write(f"__label__icons {line_text}\n")

    print(f"Built fake supervised corpus => {SUPERVISED_TXT}")

###########################################################
# 3) TRAIN SUPERVISED ON DUMMY LABEL
###########################################################
def train_and_quantize():
    # We assume you've already done 'prepare_base_model()' => SMALL_QUANT_MODEL_NAME
    # This is a compact model we can load for pretrainedVectors if we like.
    # But fastText's train_supervised doesn't accept "pretrainedVectors" as easily
    # as train_unsupervised does. We'll skip that step and just do a normal supervised train.

    build_supervised_corpus()

    print(f"Training supervised model from {SUPERVISED_TXT}")
    # We'll do a small dimension=SMALL_DIM so it matches what we already have
    # There's no direct "pretrainedVectors" param for train_supervised in python,
    # but we can at least keep dim=SMALL_DIM.
    model = fasttext.train_supervised(
        input=SUPERVISED_TXT,
        lr=LR,
        epoch=EPOCHS,
        dim=SMALL_DIM,
        label="__label__"
    )
    print("Done supervised training with dummy label.")

    # Now we can quantize
    print("Quantizing final domain model...")
    model.quantize(
        input=SUPERVISED_TXT,
        retrain=True,
        cutoff=CUTOFF
    )
    model.save_model(FINAL_MODEL)
    print(f"Saved domain model => {FINAL_MODEL}")

    # Clean up
    os.remove(SUPERVISED_TXT)

###########################################################
# 4) EMBED TEXT (IGNORE THE LABEL)
###########################################################
def embed_text(ft_model, text):
    """
    We'll just do average of word vectors ignoring the label token.
    """
    # fastText automatically ignores unknown tokens, but let's ensure no label prefix:
    tokens = [t for t in text.strip().split() if not t.startswith("__label__")]
    if not tokens:
        return np.zeros(ft_model.get_dimension(), dtype=np.float32)
    vecs = [ft_model.get_word_vector(t) for t in tokens]
    return np.mean(vecs, axis=0)

###########################################################
# 5) EMBED ICONS
###########################################################
def embed_icons():
    print(f"Loading final model => {FINAL_MODEL}")
    ft_model = fasttext.load_model(FINAL_MODEL)

    with open(ICONS_JSON_FILE, "r", encoding="utf-8") as f:
        icons_data = json.load(f)
    icons = icons_data["icons"]

    all_embs = []
    meta = []
    for icon in icons:
        text = icon["name"] + " " + icon["tags"]
        text = text.replace(",", " ")
        emb = embed_text(ft_model, text)
        all_embs.append(emb)
        meta.append({"id": icon["name"], "tags": icon["tags"]})

    all_embs = np.array(all_embs)
    np.save(ICON_EMBEDS_NPY, all_embs)
    with open(ICON_INDEX_JSON, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\nIcon embeddings => {ICON_EMBEDS_NPY}")
    print(f"Icon metadata   => {ICON_INDEX_JSON}")

###########################################################
# MAIN
###########################################################
def main():
    # Step 1) If not done yet, prepare base model => cc.en.50compact_quantized.bin
    # This step is optional if you already have it from previous runs.
    if not os.path.exists(SMALL_QUANT_MODEL_NAME):
        prepare_base_model()

    # Step 2) Train supervised with dummy label => produce domain ft model
    # train_and_quantize()

    # Step 3) Embed icons
    # embed_icons()

if __name__ == "__main__":
    main()

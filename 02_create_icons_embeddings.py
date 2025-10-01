#!/usr/bin/env python

import json
import os

import fasttext
import numpy as np
import typer

app = typer.Typer()

ROUND_DECIMALS = 3


# -------------------------------------------------------------------------
def load_fasttext_model(model_path):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Missing FastText model at: {model_path}")
    print(f"Loading FastText model: {model_path}")
    model = fasttext.load_model(model_path)
    print("Model loaded.")
    return model


def create_icon_embeddings(model, icons_json_path):
    with open(icons_json_path, "r", encoding="utf-8") as f:
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

        emb_list = [round(float(x), ROUND_DECIMALS) for x in emb]
        icon_id = icon["name"]
        icon_embeds[icon_id] = emb_list

    return icon_embeds, all_words


def create_word_vocab_embeddings(model, word_list):
    vocab_dict = {}
    for w in word_list:
        vec = model.get_word_vector(w)
        vocab_dict[w] = [round(float(x), ROUND_DECIMALS) for x in vec]
    return vocab_dict


@app.command()
def main(
        languages: str = typer.Option(..., help="Comma-separated list of language codes, e.g. 'ru,en,fr'"),
):
    """
    Create icon and word embeddings for one or more languages.
    Example: python 02_create_icons_embeddings.py --languages ru,en
    """
    lang_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
    for LANGUAGE in lang_list:
        fasttext_model_path = f".models/cc.{LANGUAGE}.200.bin"
        icons_json_path = f"data/icons.stripped.{LANGUAGE}.json"
        icon_embeddings_json = f"embeddings/icon_embeddings.{LANGUAGE}.json"
        word_embeddings_json = f"embeddings/vocab_embeddings.{LANGUAGE}.json"

        print(f"\nProcessing language: {LANGUAGE}")
        ft_model = load_fasttext_model(fasttext_model_path)
        icon_embeds, word_set = create_icon_embeddings(ft_model, icons_json_path)
        vocab_dict = create_word_vocab_embeddings(ft_model, word_set)

        with open(icon_embeddings_json, "w", encoding="utf-8") as f:
            json.dump(icon_embeds, f, ensure_ascii=False)
        print(f"Saved icon embeddings => {icon_embeddings_json}")

        with open(word_embeddings_json, "w", encoding="utf-8") as f:
            json.dump(vocab_dict, f, ensure_ascii=False)
        print(f"Saved word embeddings => {word_embeddings_json}")

        print("Done.")


if __name__ == "__main__":
    app()

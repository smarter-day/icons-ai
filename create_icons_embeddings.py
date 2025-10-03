#!/usr/bin/env python

import json
import os
from pathlib import Path
from typing import Union

import dotenv
import fasttext
import fasttext.util
import typer
from sentence_transformers import SentenceTransformer

from library.languages import load_languages
from library.project import Project
from library.settings import ProjectSettings

dotenv.load_dotenv()
app = typer.Typer()


# -------------------------------------------------------------------------
def load_model(model_name: str, model_type: str = "huggingface", models_dir: str = None):
    """Load either FastText or HuggingFace model based on type."""
    if model_type == "fasttext":
        assert models_dir is not None, "models_dir must be provided for FastText models"
        print(f"Loading FastText model: {model_name}")

        # Extract language code from model name (e.g., "cc.en.300.bin" -> "en")
        if "cc." in model_name:
            lang_code = model_name.split(".")[1]  # Extract "en" from "cc.en.300.bin"
        else:
            lang_code = "en"  # Default fallback

        # Build full path to model in models directory
        model_path = os.path.join(models_dir, model_name)

        # Download model if it doesn't exist in models directory
        if not os.path.exists(model_path):
            print(f"Model file {model_path} not found. Downloading FastText model for {lang_code}...")
            # Ensure models directory exists
            os.makedirs(models_dir, exist_ok=True)
            old_cwd = os.getcwd()
            os.chdir(models_dir)
            fasttext.util.download_model(lang_code, if_exists='ignore')
            Path(model_path + '.gz').unlink(missing_ok=True)
            os.chdir(old_cwd)

        model = fasttext.load_model(model_path)
        print("FastText model loaded.")
        return model
    else:
        print(f"Loading SentenceTransformer model: {model_name}")
        model = SentenceTransformer(model_name)
        print("SentenceTransformer model loaded.")
        return model


def create_icon_embeddings(model, icons_json_path, round_decimals, model_type="huggingface"):
    with open(icons_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    icons = data["icons"]
    print(f"Found {len(icons)} icons")

    icon_embeds = {}
    all_words = set()

    # Process icons in batches for better performance
    batch_size = 100
    for i in range(0, len(icons), batch_size):
        batch = icons[i:i + batch_size]
        texts = []

        for icon in batch:
            text = icon["name"] + " " + icon["tags"]
            texts.append(text)

            # Extract words for vocabulary
            tokens = text.replace(",", " ").strip().split()
            tokens = [t.lower() for t in tokens if t.strip()]
            all_words.update(tokens)

        # Get embeddings for the batch
        if model_type == "fasttext":
            embeddings = []
            for text in texts:
                embedding = model.get_sentence_vector(text)
                embeddings.append(embedding)
        else:
            embeddings = model.encode(texts)

        # Store embeddings
        for j, icon in enumerate(batch):
            emb_list = [round(float(x), round_decimals) for x in embeddings[j]]
            icon_id = icon["name"]
            icon_embeds[icon_id] = emb_list

    return icon_embeds, all_words


def create_word_vocab_embeddings(model, word_list, round_decimals, model_type="huggingface"):
    vocab_dict = {}
    # Process words in batches for better performance
    batch_size = 1000
    for i in range(0, len(word_list), batch_size):
        batch_words = list(word_list)[i:i + batch_size]
        if model_type == "fasttext":
            embeddings = []
            for word in batch_words:
                embedding = model.get_word_vector(word)
                embeddings.append(embedding)
        else:
            embeddings = model.encode(batch_words)

        for j, word in enumerate(batch_words):
            vocab_dict[word] = [
                round(float(x), round_decimals) for x in embeddings[j]
            ]
    return vocab_dict


@app.command()
def main(
    languages: str = typer.Option(
        None,
        "--languages",
        help="Comma-separated list of language codes, e.g. 'ru,en,fr'"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
):
    """
    Create icon and word embeddings for one or more languages.
    Example: python create_icons_embeddings.py --languages ru,en
    """
    # Load project configuration
    try:
        project = Project(project_file)
        settings = project.Settings(ProjectSettings)
    except (ValueError, FileNotFoundError) as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    # Load languages list
    lang_list = load_languages(languages=languages, settings=settings)
    if not lang_list:
        typer.echo("Error: no valid languages specified in --languages.")
        raise typer.Exit(code=1)

    for lang_code in lang_list:
        # Get language-specific settings
        lang_settings = None
        for lang in settings.languages:
            if lang.code == lang_code:
                lang_settings = lang
                break

        if not lang_settings:
            typer.echo(f"Error: no settings found for language '{lang_code}'")
            continue

        # Get round_decimals from language settings or defaults
        round_decimals = lang_settings.model.embeddings.round_decimals

        # Build file paths using project settings
        icons_json_path = settings.icons.stripped_file.format(
            language=lang_code
        )
        icon_embeddings_json = f"embeddings/icon_embeddings.{lang_code}.json"
        word_embeddings_json = f"embeddings/vocab_embeddings.{lang_code}.json"

        print(f"\nProcessing language: {lang_code}")

        # Get model type from settings (default to huggingface if not specified)
        model_type = getattr(lang_settings.model, 'type', 'huggingface')

        model = load_model(lang_settings.model.name, model_type, settings.models.dir)
        icon_embeds, word_set = create_icon_embeddings(
            model, icons_json_path, round_decimals, model_type
        )
        vocab_dict = create_word_vocab_embeddings(
            model, word_set, round_decimals, model_type
        )

        # Ensure embeddings directory exists
        Path("embeddings").mkdir(exist_ok=True)

        with open(icon_embeddings_json, "w", encoding="utf-8") as f:
            json.dump(icon_embeds, f, ensure_ascii=False)
        print(f"Saved icon embeddings => {icon_embeddings_json}")

        with open(word_embeddings_json, "w", encoding="utf-8") as f:
            json.dump(vocab_dict, f, ensure_ascii=False)
        print(f"Saved word embeddings => {word_embeddings_json}")

        print("Done.")


if __name__ == "__main__":
    app()

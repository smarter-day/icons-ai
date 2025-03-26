#!/usr/bin/env python3

import os

import dotenv
import fasttext
import fasttext.util
import typer
import yaml

dotenv.load_dotenv()
app = typer.Typer()

DEFAULT_PROJECT = os.environ.get("DEFAULT_PROJECT")
MODELS_DIR = ".models"

@app.command()
def prepare_model(
    languages: str = typer.Option(..., "--languages", help="Comma-separated language codes, e.g. en,ru"),
    default_dim: int = typer.Option(None, "--default-dim", help="Override base dimension before reduction"),
    small_dim: int = typer.Option(None, "--small-dim", help="Override dimension after reduction"),
    project: str = typer.Option(DEFAULT_PROJECT, "--project", help="Path to the project YAML config")
):
    """
    Reads project.yaml, merges top-level defaults with language-specific overrides
    plus any CLI overrides, and for each language in --languages:
      1) Download cc.{lang}.{final_default_dim}.bin into ./.models (if missing)
      2) Dimension-reduce to final_small_dim (if missing)
      3) Save cc.{lang}.{final_small_dim}.bin in ./.models
    """

    # 1) Parse comma-separated languages => list
    lang_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
    if not lang_list:
        typer.echo("Error: no valid languages specified in --languages.")
        raise typer.Exit(code=1)

    # 2) Check project file
    if not project or not os.path.exists(project):
        typer.echo(f"Error: project file not found: {project}")
        raise typer.Exit(code=1)

    # 3) Load YAML
    with open(project, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f) or {}

    # Top-level defaults
    defaults = config_data.get("defaults", {})
    yaml_default_dim = defaults.get("default_dim", 300)
    yaml_small_dim = defaults.get("small_dim", 150)

    # Language-specific list
    yaml_langs = config_data.get("languages", [])

    # Build a dict: {lang_code: (local_def_dim, local_small_dim)}
    # If the language in YAML doesn't specify dims, fallback to top-level
    lang_dim_map = {}
    for entry in yaml_langs:
        code = entry.get("code")
        if not code:
            continue
        local_def_dim = entry.get("default_dim", yaml_default_dim)
        local_small_dim = entry.get("small_dim", yaml_small_dim)
        lang_dim_map[code] = (local_def_dim, local_small_dim)

    # Ensure .models exists
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 4) Progress bar over the languages
    with typer.progressbar(lang_list, label="Processing languages") as progress:
        for lang in progress:
            if lang not in lang_dim_map:
                typer.echo(f"Warning: language '{lang}' not found in project.yaml 'languages'. Skipping.")
                continue

            local_def_dim, local_small_dim = lang_dim_map[lang]

            # final dims = CLI override > language override > top-level
            final_default_dim = default_dim if default_dim is not None else local_def_dim
            final_small_dim = small_dim if small_dim is not None else local_small_dim

            typer.echo(
                f"\n--- Preparing model for lang='{lang}' => default_dim={final_default_dim}, small_dim={final_small_dim}"
            )

            # Paths in .models
            base_model_name = f"cc.{lang}.{final_default_dim}.bin"
            base_model_path = os.path.join(MODELS_DIR, base_model_name)

            reduced_model_name = f"cc.{lang}.{final_small_dim}.bin"
            reduced_model_path = os.path.join(MODELS_DIR, reduced_model_name)

            # 5) Download if needed
            if os.path.exists(base_model_path):
                typer.echo(f"Base model already exists: {base_model_path} - skipping download.")
            else:
                typer.echo(f"Downloading {base_model_name} into {MODELS_DIR}...")
                # Temporarily chdir so fasttext places files in .models
                old_cwd = os.getcwd()
                os.chdir(MODELS_DIR)
                fasttext.util.download_model(lang, if_exists="ignore")
                os.chdir(old_cwd)

                if not os.path.exists(base_model_path):
                    typer.echo(f"Error: Could not find {base_model_path} after download attempt.")
                    continue

            # 6) Reduce if needed
            if os.path.exists(reduced_model_path):
                typer.echo(f"Reduced model already exists: {reduced_model_path} - skipping reduce.")
            else:
                typer.echo(f"Loading base model: {base_model_path}")
                model = fasttext.load_model(base_model_path)
                typer.echo(f"Reducing dimension from {final_default_dim} => {final_small_dim} ...")
                fasttext.util.reduce_model(model, final_small_dim)

                typer.echo(f"Saving reduced model => {reduced_model_path}")
                model.save_model(reduced_model_path)

    typer.echo("\nAll done!")

def main():
    app()

if __name__ == "__main__":
    main()

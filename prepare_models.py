#!/usr/bin/env python3

import os

import fasttext
import fasttext.util
import typer

from library.languages import load_languages
from library.project import Project
from library.settings import PrepareModelSettings

app = typer.Typer()


@app.command()
def prepare_model(
    languages: str = typer.Option(
        None,
        "--languages",
        help="Comma-separated language codes to process, e.g. 'en,ru'"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
):
    """
    Prepare FastText models for icon search by downloading and reducing
    dimensions.

    For each language in --languages:
    1) Download cc.{lang}.{base_dim}.bin into models directory (if missing)
    2) Dimension-reduce from base_dim to distilled_dim (if missing)
    3) Save cc.{lang}.{distilled_dim}.bin in models directory
    """
    try:
        project = Project(project_file)
        settings = project.Settings(PrepareModelSettings)
    except (ValueError, FileNotFoundError) as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    lang_list = load_languages(languages=languages, settings=settings)
    if not lang_list:
        typer.echo("Error: no valid languages specified in --languages.")
        raise typer.Exit(code=1)

    # Build a dict: {lang_code: (base_dim, distilled_dim)}
    lang_dim_map = {}
    for lang_settings in settings.languages:
        lang_code = lang_settings.code
        base_dim = lang_settings.model.base_dim
        distilled_dim = lang_settings.model.distilled_dim
        lang_dim_map[lang_code] = (base_dim, distilled_dim)

    # Ensure .models exists
    os.makedirs(settings.models.dir, exist_ok=True)

    # 3) Progress bar over the languages
    with typer.progressbar(
        lang_list, label="Processing languages"
    ) as progress:
        for lang in progress:
            if lang not in lang_dim_map:
                typer.echo(
                    f"Warning: language '{lang}' not found in "
                    f"project.yaml 'languages'. Skipping."
                )
                continue

            final_default_dim, final_small_dim = lang_dim_map[lang]

            typer.echo(
                f"\n--- Preparing model for lang='{lang}' => "
                f"default_dim={final_default_dim}, small_dim={final_small_dim}"
            )

            # Paths in .models
            base_model_name = f"cc.{lang}.{final_default_dim}.bin"
            base_model_path = os.path.join(settings.models.dir,
                                           base_model_name)

            reduced_model_name = f"cc.{lang}.{final_small_dim}.bin"
            reduced_model_path = os.path.join(settings.models.dir,
                                              reduced_model_name)

            # 5) Download if needed
            typer.echo(f"Checking if {base_model_path} exists...")
            if os.path.exists(base_model_path):
                typer.echo(
                    f"Base model already exists: {base_model_path} - "
                    f"skipping download."
                )
            else:
                typer.echo(
                    f"Downloading {base_model_name} into "
                    f"{settings.models.dir}..."
                )
                # Temporarily chdir so fasttext places files in .models
                old_cwd = os.getcwd()
                os.chdir(settings.models.dir)
                fasttext.util.download_model(lang, if_exists="ignore")
                os.chdir(old_cwd)

                if not os.path.exists(base_model_path):
                    typer.echo(
                        f"Error: Could not find {base_model_path} after "
                        f"download attempt."
                    )
                    continue

            # 6) Reduce if needed
            if os.path.exists(reduced_model_path):
                typer.echo(
                    f"Reduced model already exists: {reduced_model_path} - "
                    f"skipping reduce."
                )
            else:
                typer.echo(f"Loading base model: {base_model_path}")
                model = fasttext.load_model(base_model_path)
                typer.echo(
                    f"Reducing dimension from {final_default_dim} => "
                    f"{final_small_dim} ..."
                )
                fasttext.util.reduce_model(model, final_small_dim)

                typer.echo(f"Saving reduced model => {reduced_model_path}")
                model.save_model(reduced_model_path)

    typer.echo("\nAll done!")


def main():
    app()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import os
from pathlib import Path

import dotenv
import typer

from library.ai import fits_context
from library.chunking import next_chunk_size
from library.languages import load_languages
from library.project import Project
from library.settings import ProjectSettings
from library.translations import (load_existing_translations,
                                  save_translations, translate_chunk_retry)

dotenv.load_dotenv()
app = typer.Typer()


###############################################################################
# Main Command
###############################################################################

@app.command()
def translate_keywords(
    source_file: str = typer.Option(
        None,
        "--source-file",
        help="Path to source JSON (overrides project settings)"
    ),
    languages: str = typer.Option(
        None,
        "--languages",
        help="Comma-separated list of languages (e.g., 'ru,fr')"
    ),
    openai_api_key: str = typer.Option(
        None,
        "--openai-api-key",
        help="OpenAI API key (overrides OPENAI_API_KEY env var)"
    ),
    model: str = typer.Option(
        None,
        "--model",
        help="OpenAI model to use (overrides project settings)"
    ),
    context_window: int = typer.Option(
        None,
        "--context-window",
        help="Context window size (overrides project settings)"
    ),
    max_tokens: int = typer.Option(
        None,
        "--max-tokens",
        help="Maximum tokens for response (overrides project settings)"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
):
    """
    Translates tags from the source file into specified languages.

    Uses project configuration to determine source file and languages if not
    specified. Supports multiple languages and project configuration.
    Dynamically adjusts the chunk size so as not to exceed GPT's context limit.
    Updates the target translation file with successful translations.
    """
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

    # Filter out English since we don't need to translate English to English
    lang_list = [lang for lang in lang_list if lang != "en"]
    if not lang_list:
        typer.echo("No non-English languages to translate."
                   "Skipping translation.")
        return

    # Use project settings if source_file not provided
    if source_file is None:
        source_file = settings.icons.stripped_file.format(language="en")

    # Load translation settings from project (with command line overrides)
    model = model or settings.translation.model
    context_window = context_window or settings.translation.context_window
    max_tokens = max_tokens or settings.translation.max_tokens

    # Validate API key.
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        typer.echo("Error: OPENAI_API_KEY is missing")
        raise typer.Exit(code=1)

    # Load source data.
    src_path = Path(source_file)
    if not src_path.exists():
        typer.echo(f"Error: Source file not found: {src_path}")
        raise typer.Exit(code=1)
    with src_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    icons = data.get("icons", [])
    all_tags = sorted(set(
        tag.strip()
        for icon in icons
        for tag in icon.get("tags", "").split(",")
        if tag.strip()
    ))
    typer.echo(f"Found {len(all_tags)} unique tags total in {source_file}.")

    # Process each language.
    for lang_code in lang_list:
        language_label = f"{lang_code} language"
        # Use project settings with language placeholder
        target_template = settings.translation.file
        out_file = Path(target_template.format(language=lang_code))
        existing_map = load_existing_translations(out_file)

        # Build list of tags that still need translation.
        to_translate = [t for t in all_tags if t not in existing_map]
        if not to_translate:
            typer.echo(f"All tags translated for '{lang_code}'. Skipping.")
            continue

        total_left = len(to_translate)
        typer.echo(f"\nTranslating {total_left} tags into '{lang_code}' => {out_file}")
        with typer.progressbar(length=total_left, label=f"Translating => {lang_code}") as pbar:
            # Initialize current_chunk_size based on the remaining list.
            def fits_context_wrapper(chunk):
                return fits_context(chunk, language_label, max_tokens, context_window)
            current_chunk_size = next_chunk_size(to_translate, fits_context_wrapper)
            if current_chunk_size == 0:
                current_chunk_size = 1

            while to_translate:
                if current_chunk_size > len(to_translate):
                    current_chunk_size = len(to_translate)
                chunk = to_translate[:current_chunk_size]
                typer.echo(f"\nTranslating chunk of {len(chunk)} keywords")
                partial_map = translate_chunk_retry(chunk, language_label, api_key, model, max_tokens)

                if partial_map:
                    # Update target dictionary with translations.
                    for k, v in partial_map.items():
                        existing_map[k] = v
                    save_translations(out_file, existing_map)

                    # Determine which items in the chunk were translated.
                    translated = [item for item in chunk if item in partial_map]
                    pbar.update(len(translated))
                    typer.echo(f"Translated {len(translated)} keywords from chunk.")

                    # Remove translated items from the list.
                    # (Keep items not translated at the front.)
                    to_translate = [item for item in chunk if item not in partial_map] + to_translate[
                        current_chunk_size:]

                    if len(translated) < len(chunk):
                        # Partial success: shrink chunk size.
                        current_chunk_size = max(1, current_chunk_size // 2)
                        typer.echo(f"Partial success. Reduced chunk size to {current_chunk_size}.")
                    else:
                        # Full success: try increasing chunk size slightly.
                        recalculated = next_chunk_size(to_translate, fits_context_wrapper)
                        current_chunk_size = max(1, int((current_chunk_size + recalculated) / 2))
                        typer.echo(f"Full success. Adjusted chunk size to {current_chunk_size}.")
                else:
                    # No translation obtained.
                    if current_chunk_size == 1:
                        typer.echo(f"Skipping item '{chunk[0]}' due to repeated failures.")
                        pbar.update(1)
                        to_translate = to_translate[1:]
                    else:
                        current_chunk_size = max(1, current_chunk_size // 2)
                        typer.echo(f"No success. Reduced chunk size to {current_chunk_size}.")

        typer.echo(f"Finished translating '{lang_code}' => {out_file}")


if __name__ == "__main__":
    app()

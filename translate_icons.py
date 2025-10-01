#!/usr/bin/env python3
import json
from pathlib import Path

import dotenv
import typer

from library.languages import load_languages
from library.project import Project
from library.settings import ProjectSettings

dotenv.load_dotenv()
app = typer.Typer()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.command()
def translate_icons(
    english_icons_file: str = typer.Option(
        None,
        "--english-icons-file",
        help="Path to the English stripped icons JSON file "
        "(overrides project settings), "
        "Example: data/icons.stripped.en.json"
    ),
    languages: str = typer.Option(
        None,
        "--languages",
        help="Comma-separated list of languages (e.g., 'ru,fr')"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
):
    """
    For each icon in the provided English stripped icons file,
    replace each tag in the 'tags'
    field with its translation loaded from data/keywords.<language>.json.
    Unknown tags (i.e. not found in the translation dictionary)
    are printed as an ordered list to the console.

    The translated icons JSON is written in the same folder as the source file,
    with the file name suffix replaced by '.<language>.json'.
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

    # Filter out English since we don't need to translate English to English
    lang_list = [lang for lang in lang_list if lang != "en"]
    if not lang_list:
        typer.echo("No non-English languages to translate. "
                   "Skipping translation.")
        return

    # Use project settings if english_icons_file not provided
    if english_icons_file is None:
        english_icons_file = settings.icons.stripped_file.format(language="en")

    source_path = Path(english_icons_file)
    if not source_path.exists():
        typer.echo(f"Error: File '{english_icons_file}' not found.")
        raise typer.Exit(code=1)

    # Load the original icons JSON
    icons_data = load_json(source_path)
    icons = icons_data.get("icons", [])
    if not icons:
        typer.echo("No icons found in the file.")
        raise typer.Exit(code=1)

    # Process each language separately
    for lang in lang_list:
        # Use project settings for translation file path
        translation_file = Path(
            settings.translation.file.format(language=lang)
        )
        if not translation_file.exists():
            typer.echo(f"Translation file '{translation_file}' "
                       f"not found for language '{lang}'. Skipping.")
            continue

        translations = load_json(translation_file)
        unknown_tags = set()

        # Process each icon and update its tags
        for icon in icons:
            tag_str = icon.get("tags", "")
            # Split by comma and strip whitespace
            tags = [t.strip() for t in tag_str.split(",") if t.strip()]
            translated_tags = []
            for tag in tags:
                if tag in translations:
                    translated_tags.append(translations[tag])
                else:
                    translated_tags.append(tag)
                    unknown_tags.add(tag)
            # Rejoin the translated tags into a string
            icon["tags"] = ",".join(translated_tags)

        # Output unknown tags as an ordered list
        if unknown_tags:
            typer.echo(f"\nUnknown tags for language '{lang}':")
            for idx, tag in enumerate(sorted(unknown_tags), start=1):
                typer.echo(f"{idx}. {tag}")
        else:
            typer.echo(f"\nAll tags translated for language '{lang}'.")

        # Construct output file path:
        # original stem + ".<lang>" + original suffix.
        output_file = (source_path.parent /
                       f"{source_path.stem.replace('.en', '')}"
                       f".{lang}{source_path.suffix}")
        save_json(output_file, icons_data)
        typer.echo(f"Translated icons for '{lang}' saved to: {output_file}")


if __name__ == "__main__":
    app()

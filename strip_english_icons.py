#!/usr/bin/env python3

import json
from pathlib import Path

import typer

from library.project import Project
from library.settings import ProjectSettings

app = typer.Typer()


@app.command()
def strip_icons(
    source_file: str = typer.Option(
        None,
        "--source-file",
        help="Path to the English icons JSON (overrides project settings)"
    ),
    target_file: str = typer.Option(
        None,
        "--target-file",
        help="Path for the stripped English icons output "
        "(overrides project settings)"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
):
    """
    Reads an English icons JSON, transforms it so each icon has ONLY 'tags' and 'name',
    then saves to <original_basename>.stripped.en.json in the same folder.

    Uses project configuration to determine source and target files if not
    specified. Always processes English icons only.
    """
    try:
        project = Project(project_file)
        settings = project.Settings(ProjectSettings)
    except (ValueError, FileNotFoundError) as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    # Use project settings if source_file not provided
    if source_file is None:
        source_file = settings.icons.source_file

    src_path = Path(source_file)
    if not src_path.exists():
        typer.echo(f"Error: file not found: {source_file}")
        raise typer.Exit(code=1)

    # Load icons
    with src_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    icons = data.get("icons", [])
    typer.echo(f"Loaded {len(icons)} icons from '{source_file}'.")

    # Transform
    stripped_icons = []
    for icon in icons:
        stripped_icons.append({
            "name": icon["name"],
            "tags": icon["tags"]
        })

    # Build output structure
    result = {"icons": stripped_icons}

    # Use target_file if provided, otherwise use project settings for English
    if target_file:
        out_path = Path(target_file)
    else:
        # Use project settings with English language placeholder
        target_template = settings.icons.stripped_file
        target_path = target_template.format(language="en")
        out_path = Path(target_path)

    # Write to the new file
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    typer.echo(f"Saved stripped English icons => {out_path}")


def main():
    app()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import os
import typer
from pathlib import Path

app = typer.Typer()

@app.command()
def strip_icons(
    source_file: str = typer.Option("data/icons.json", "--source-file", help="Path to the icons JSON")
):
    """
    Reads an icons JSON, transforms it so each icon has ONLY 'tags' and 'name',
    then saves to <original_basename>.stripped.json in the same folder.
    """
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

    # Determine output file => "original_name.stripped.json"
    out_path = src_path.parent / f"{src_path.stem}.stripped.json"

    # Write to the new file
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    typer.echo(f"Saved stripped icons => {out_path}")

def main():
    app()

if __name__ == "__main__":
    main()

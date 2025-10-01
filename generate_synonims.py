#!/usr/bin/env python3
import json
from pathlib import Path
import typer

# Ensure NLTK WordNet is available
try:
    from nltk.corpus import wordnet
except ImportError:
    typer.echo("Missing NLTK WordNet. Please install nltk and run: python -m nltk.downloader wordnet")
    raise

app = typer.Typer()


def generate_synonyms(tag: str, count: int) -> list[str]:
    """
    Generate up to `count` synonyms for a given tag using WordNet.
    Skips multi-word tags.
    """
    tag_clean = tag.lower().strip()
    if not tag_clean or " " in tag_clean:
        return []
    synonyms = set()
    for syn in wordnet.synsets(tag_clean):
        for lemma in syn.lemmas():
            word = lemma.name().replace("_", " ").lower().strip()
            if word != tag_clean:
                synonyms.add(word)
    # Return sorted list of synonyms (alphabetically) limited to count
    return sorted(synonyms)[:count]


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.command()
def add_synonyms(
        icons_file: str = typer.Option("data/icons.stripped.en.json", help="Path to the icons JSON file"),
        synonyms_count: int = typer.Option(50, help="Number of synonyms to generate for each tag")
):
    """
    Reads an icons JSON file, and for each tag in each icon generates up to X synonyms
    (using NLTK WordNet) and appends them to the existing tags.

    The resulting tags will not contain duplicates and are limited to a maximum of 50 tags.
    The updated JSON is saved back to the same file.
    """
    file_path = Path(icons_file)
    if not file_path.exists():
        typer.echo(f"Error: File '{icons_file}' not found.")
        raise typer.Exit(code=1)

    data = load_json(file_path)
    icons = data.get("icons", [])
    if not icons:
        typer.echo("No icons found in the file.")
        raise typer.Exit(code=1)

    for icon in icons:
        tag_str = icon.get("tags", "")
        # Split the comma-separated tags and remove extra whitespace
        original_tags = [tag.strip() for tag in tag_str.split(",") if tag.strip()]
        # Use a set to avoid duplicates (includes original tags)
        combined_tags = set(original_tags)
        for tag in original_tags:
            syns = generate_synonyms(tag, synonyms_count)
            combined_tags.update(syns)
        # Limit total tags to 50 and sort alphabetically
        final_tags = sorted(combined_tags)[:50]
        icon["tags"] = ",".join(final_tags)

    save_json(file_path, data)
    typer.echo(f"Updated icons file saved to: {file_path}")


if __name__ == "__main__":
    app()

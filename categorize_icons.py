#!/usr/bin/env python3
import json
import os
from pathlib import Path

import typer
from sentence_transformers import SentenceTransformer, util

from library.project import Project
from library.settings import ProjectSettings

# Categories for daily life relevance
# These are carefully selected based on common daily task categories in productivity apps
# like Todoist, Notion, or Google Calendar. They cover typical areas for regular people:
# family life, social interactions, professional duties, personal well-being, finances,
# learning, errands, travel, home management, meals, leisure, pets, scheduling, self-care,
# and tech-related tasks. I aimed for 15 categories to provide broad coverage without
# overlap, focusing on everyday relevance for task management and calendar events.
CATEGORIES = [
    "Family and Relationships",  # e.g., kids, spouse, family events
    "Friends and Social",        # e.g., hangouts, parties, networking
    "Work and Career",           # e.g., meetings, projects, office tasks
    "Health and Fitness",        # e.g., exercise, doctor visits, wellness
    "Finance and Money",         # e.g., bills, budgeting, investments
    "Education and Learning",    # e.g., classes, studying, skill-building
    "Shopping and Errands",      # e.g., groceries, purchases, daily chores
    "Travel and Transportation",  # e.g., trips, commuting, vacations
    "Home and Chores",           # e.g., cleaning, repairs, household management
    "Food and Cooking",          # e.g., meals, recipes, dining out
    "Hobbies and Entertainment",  # e.g., reading, movies, gaming
    "Pets and Animals",          # e.g., vet visits, pet care
    "Events and Calendar",       # e.g., appointments, reminders, holidays
    "Personal Care",             # e.g., grooming, relaxation, self-improvement
    "Technology and Gadgets"     # e.g., device setup, apps, tech support
]

app = typer.Typer()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.command()
def categorize_icons(
    stripped_icons_file: str = typer.Option(
        None,
        "--stripped-icons-file",
        help="Path to the stripped icons JSON file (overrides project settings)"
    ),
    threshold: float = typer.Option(
        None,
        "--threshold",
        help="Similarity threshold for enabling icons (0.0-1.0, higher = more strict, overrides project settings)"
    ),
    model_name: str = typer.Option(
        None,
        "--model",
        help="Sentence transformer model name for semantic similarity"
    ),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (overrides DEFAULT_PROJECT)"
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force re-categorization even if enabled icons file already exists"
    ),
):
    """
    Categorizes stripped icons based on semantic similarity to daily life categories.

    Uses sentence transformers to compute semantic similarity between icon names/tags
    and predefined categories for daily life activities. Icons are marked as 'enabled'
    if their similarity to any category exceeds the threshold.

    The updated JSON is saved back to the same file with an 'enabled' flag for each icon.
    Works with the primary language icons from project settings.
    """
    try:
        project = Project(project_file)
        settings = project.Settings(ProjectSettings)
    except (ValueError, FileNotFoundError) as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    # Get primary language for file path
    primary_language = None
    for lang in settings.languages:
        if lang.type == "primary":
            primary_language = lang.code
            break

    if primary_language is None:
        typer.echo("Error: No primary language found in project settings.")
        raise typer.Exit(code=1)

    # Use project settings if parameters not provided
    if stripped_icons_file is None:
        # Use project settings with primary language placeholder
        target_template = settings.icons.stripped_file
        icons_file_path = target_template.format(language=primary_language)
    else:
        icons_file_path = stripped_icons_file

    # Create output path for enabled icons
    enabled_icons_path = f"data/icons.enabled.{primary_language}.json"

    # Check if enabled icons file already exists
    if not force and os.path.exists(enabled_icons_path):
        typer.echo(f"Enabled icons file already exists: {enabled_icons_path}")
        typer.echo("Use --force to re-categorize and overwrite existing file")

        # Show some stats about the existing file
        try:
            with open(enabled_icons_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
            existing_count = len(existing_data.get("icons", []))
            typer.echo(f"Existing file contains {existing_count} enabled icons")
        except Exception as e:
            typer.echo(f"Could not read existing file: {e}")

        return

    effective_threshold = threshold
    if effective_threshold is None:
        # Use categorization threshold from project settings
        effective_threshold = settings.models.defaults.categorization.threshold

    effective_model = model_name
    if effective_model is None:
        # Use categorization model from project settings
        effective_model = settings.models.defaults.categorization.model

    file_path = Path(icons_file_path)
    if not file_path.exists():
        typer.echo(f"Error: File '{icons_file_path}' not found.")
        raise typer.Exit(code=1)

    typer.echo(f"Loading model: {effective_model}")
    model = SentenceTransformer(effective_model)

    typer.echo("Computing category embeddings...")
    category_embeddings = model.encode(CATEGORIES)

    typer.echo(f"Loading icons from: {file_path}")
    data = load_json(file_path)
    icons = data.get("icons", [])
    if not icons:
        typer.echo("No icons found in the file.")
        raise typer.Exit(code=1)

    typer.echo(f"Processing {len(icons)} {primary_language} icons with threshold {effective_threshold}...")

    enabled_icons = []
    categorized_icons = {}

    for icon in icons:
        # Combine name and tags into one text for better context
        text = icon['name'] + ', ' + icon['tags']
        icon_embedding = model.encode(text)

        # Compute cosine similarities to all categories
        similarities = util.cos_sim(icon_embedding, category_embeddings)[0]

        # Get the maximum similarity score and find the best category
        max_similarity = max(similarities)
        best_category_idx = similarities.argmax()
        best_category = CATEGORIES[best_category_idx]

        # Mark as enabled if relevant enough
        is_enabled = max_similarity > effective_threshold
        if is_enabled:
            # Only include enabled icons in the output
            enabled_icons.append(icon)
        
        # Store the category assignment with weight for all icons
        categorized_icons[icon['name']] = {
            "weight": float(max_similarity),
            "category": best_category
        }

    # Save enabled icons to separate file
    enabled_data = {"icons": enabled_icons}
    enabled_file_path = Path(enabled_icons_path)
    save_json(enabled_file_path, enabled_data)

    # Save categories.json file
    categories_data = {
        "categories": CATEGORIES,
        "categorized_icons": categorized_icons
    }
    categories_file_path = Path("data/categories.json")
    save_json(categories_file_path, categories_data)

    total_icons = len(icons)
    enabled_count = len(enabled_icons)
    typer.echo(f"Results: {enabled_count}/{total_icons} icons enabled ({(enabled_count / total_icons) * 100:.2f}%)")
    typer.echo(f"Enabled {primary_language} icons saved to: {enabled_icons_path}")
    typer.echo(f"Categories data saved to: {categories_file_path}")


if __name__ == "__main__":
    app()

#!/usr/bin/env python3
"""Rewrite Create ML project dataset URLs for the current clone location."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = ROOT / "IconsClassifier.mlproj"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Update dataURL references inside a Create ML .mlproj package so the "
            "project can be opened from the current repository clone."
        )
    )
    parser.add_argument(
        "--project",
        type=Path,
        default=DEFAULT_PROJECT,
        help=f"Path to the .mlproj package. Default: {DEFAULT_PROJECT}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the files that would be changed without writing them.",
    )
    return parser.parse_args()


def file_url_to_repo_path(value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme != "file":
        return None

    path = Path(unquote(parsed.path))
    if "merged_icons_dataset" not in path.parts:
        return None

    index = path.parts.index("merged_icons_dataset")
    return ROOT.joinpath(*path.parts[index:])


def relocate_json(value: object, project_dir: Path) -> tuple[object, int]:
    changes = 0

    if isinstance(value, dict):
        updated: dict[object, object] = {}
        for key, item in value.items():
            if key == "dataURL" and isinstance(item, str):
                dataset_path = file_url_to_repo_path(item)
                if dataset_path is not None:
                    new_value = dataset_path.resolve().as_uri()
                    if new_value != item:
                        updated[key] = new_value
                        changes += 1
                        continue

            if key == "dataPathRelativeToProjectURL" and isinstance(item, str):
                dataset_path = file_url_to_repo_path(value.get("dataURL", ""))
                if dataset_path is not None:
                    rel_path = Path(
                        os.path.relpath(
                            dataset_path.resolve(),
                            project_dir.resolve(),
                        )
                    )
                    new_value = rel_path.as_posix()
                    if item.endswith("/") and not new_value.endswith("/"):
                        new_value += "/"
                    if new_value != item:
                        updated[key] = new_value
                        changes += 1
                        continue

            new_item, nested_changes = relocate_json(item, project_dir)
            updated[key] = new_item
            changes += nested_changes
        return updated, changes

    if isinstance(value, list):
        updated_list = []
        for item in value:
            new_item, nested_changes = relocate_json(item, project_dir)
            updated_list.append(new_item)
            changes += nested_changes
        return updated_list, changes

    return value, changes


def display_path(path: Path, project_dir: Path) -> str:
    try:
        return str(path.relative_to(project_dir.parent))
    except ValueError:
        return str(path)


def main() -> None:
    args = parse_args()
    project_dir = args.project.resolve()

    if not project_dir.exists():
        raise SystemExit(f"Project does not exist: {project_dir}")
    if not project_dir.is_dir():
        raise SystemExit(f"Expected a .mlproj package directory: {project_dir}")

    json_files = sorted(project_dir.rglob("*.json"))
    changed_files: list[tuple[Path, int]] = []

    for path in json_files:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        updated, changes = relocate_json(data, project_dir)
        if not changes:
            continue

        changed_files.append((path, changes))
        if args.dry_run:
            continue

        with path.open("w", encoding="utf-8") as handle:
            json.dump(updated, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

    if not changed_files:
        print(f"No dataset URL changes needed in {project_dir}")
        return

    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {len(changed_files)} file(s) in {project_dir}:")
    for path, changes in changed_files:
        print(f"  {display_path(path, project_dir)} ({changes} change(s))")


if __name__ == "__main__":
    main()

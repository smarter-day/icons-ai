#!/usr/bin/env python3
"""Remove exact duplicate train texts inside a semantic icon group."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
GROUPS_PATH = ROOT / "docs" / "icon-semantic-groups.yml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove exact duplicate train texts shared by multiple icons in one semantic group."
    )
    parser.add_argument("--group", required=True, help="Semantic group name from docs/icon-semantic-groups.yml")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without rewriting files.")
    return parser.parse_args()


def parse_groups(path: Path) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    current_name: str | None = None
    in_icons = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if line.startswith("  - name: "):
            current_name = stripped.split(": ", 1)[1]
            groups[current_name] = []
            in_icons = False
            continue

        if current_name is None:
            continue

        if line.startswith("    icons:"):
            in_icons = True
            continue

        if in_icons and line.startswith("      - "):
            groups[current_name].append(stripped[2:].strip())
            continue

        if in_icons and not line.startswith("      - "):
            in_icons = False

    return groups


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def clean_group(group_name: str, dry_run: bool) -> dict[str, object]:
    groups = parse_groups(GROUPS_PATH)
    if group_name not in groups:
        raise SystemExit(f"Unknown group: {group_name}")

    icons = groups[group_name]
    report: dict[str, object] = {"group": group_name, "languages": {}}

    for lang in ("en", "ru"):
        text_to_icons: dict[str, set[str]] = defaultdict(set)
        text_locations: dict[tuple[str, str], list[int]] = defaultdict(list)
        icon_rows: dict[str, list[dict[str, str]]] = {}

        for icon in icons:
            path = ICONS_DIR / icon / f"train_{lang}.csv"
            if not path.exists():
                continue
            rows = read_rows(path)
            icon_rows[icon] = rows
            for idx, row in enumerate(rows):
                text = row["text"].strip()
                text_to_icons[text].add(icon)
                text_locations[(icon, text)].append(idx)

        duplicated = {text for text, labels in text_to_icons.items() if len(labels) >= 2}
        lang_report = {"icons_changed": 0, "rows_removed": 0, "changes": []}

        for icon, rows in icon_rows.items():
            remove_indices = {
                idx
                for text in duplicated
                for idx in text_locations.get((icon, text), [])
            }
            if not remove_indices:
                continue

            filtered = [row for idx, row in enumerate(rows) if idx not in remove_indices]
            removed_texts = [rows[idx]["text"].strip() for idx in sorted(remove_indices)]

            if not dry_run:
                write_rows(ICONS_DIR / icon / f"train_{lang}.csv", filtered)

            lang_report["icons_changed"] += 1
            lang_report["rows_removed"] += len(remove_indices)
            lang_report["changes"].append(
                {
                    "icon": icon,
                    "removed_count": len(remove_indices),
                    "removed_texts": removed_texts,
                }
            )

        report["languages"][lang] = lang_report

    return report


def main() -> None:
    args = parse_args()
    report = clean_group(args.group, args.dry_run)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

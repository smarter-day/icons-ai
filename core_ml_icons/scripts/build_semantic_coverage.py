#!/usr/bin/env python3
"""Build full semantic coverage for all icon datasets."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
GROUPS_PATH = ROOT / "docs" / "icon-semantic-groups.yml"
OUTPUT_PATH = ROOT / "docs" / "icon-semantic-coverage.json"


def parse_groups(path: Path) -> tuple[list[dict[str, object]], set[str]]:
    groups: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    in_icons = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if line.startswith("  - name: "):
            if current:
                groups.append(current)
            current = {
                "name": stripped.split(": ", 1)[1],
                "priority": "",
                "icons": [],
            }
            in_icons = False
            continue

        if current is None:
            continue

        if line.startswith("    priority: "):
            current["priority"] = stripped.split(": ", 1)[1]
            continue

        if line.startswith("    icons:"):
            in_icons = True
            continue

        if in_icons and line.startswith("      - "):
            current["icons"].append(stripped[2:].strip())
            continue

        if in_icons and not line.startswith("      - "):
            in_icons = False

    if current:
        groups.append(current)

    covered = {icon for group in groups for icon in group["icons"]}
    return groups, covered


def load_pair_risks(icons_dir: Path) -> tuple[Counter[tuple[str, str]], dict[str, list[dict[str, object]]]]:
    text_to_labels: dict[str, set[str]] = defaultdict(set)
    pair_counts: Counter[tuple[str, str]] = Counter()

    for icon_dir in sorted(path for path in icons_dir.iterdir() if path.is_dir()):
        for split in ("train_en.csv", "valid_en.csv", "test_en.csv"):
            path = icon_dir / split
            if not path.exists():
                continue
            with path.open("r", encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle)
                for row in reader:
                    text_to_labels[row["text"].strip()].add(row["label"].strip())

    for labels in text_to_labels.values():
        if len(labels) < 2:
            continue
        for a, b in combinations(sorted(labels), 2):
            pair_counts[(a, b)] += 1

    icon_pairs: dict[str, list[dict[str, object]]] = defaultdict(list)
    for (left, right), overlap in pair_counts.items():
        if overlap < 4:
            continue
        icon_pairs[left].append({"neighbor": right, "shared_text_count": overlap})
        icon_pairs[right].append({"neighbor": left, "shared_text_count": overlap})

    for pairs in icon_pairs.values():
        pairs.sort(key=lambda item: (-int(item["shared_text_count"]), str(item["neighbor"])))

    return pair_counts, icon_pairs


def build_coverage() -> dict[str, object]:
    groups, covered_by_groups = parse_groups(GROUPS_PATH)
    _, icon_pairs = load_pair_risks(ICONS_DIR)
    all_icons = sorted(path.name for path in ICONS_DIR.iterdir() if path.is_dir())

    grouped: list[dict[str, object]] = []
    pair_risk: list[dict[str, object]] = []
    isolated: list[str] = []

    icon_to_group = {}
    for group in groups:
        for icon in group["icons"]:
            icon_to_group[icon] = {
                "group": group["name"],
                "priority": group["priority"],
            }

    for icon in all_icons:
        if icon in covered_by_groups:
            grouped.append(
                {
                    "icon": icon,
                    "group": icon_to_group[icon]["group"],
                    "priority": icon_to_group[icon]["priority"],
                }
            )
            continue

        neighbors = icon_pairs.get(icon, [])
        if neighbors:
            pair_risk.append(
                {
                    "icon": icon,
                    "neighbors": neighbors[:6],
                }
            )
        else:
            isolated.append(icon)

    grouped.sort(key=lambda item: (str(item["group"]), str(item["icon"])))
    pair_risk.sort(key=lambda item: (-int(item["neighbors"][0]["shared_text_count"]), str(item["icon"])))
    isolated.sort()

    return {
        "version": 1,
        "updated": "2026-03-10",
        "source_groups_file": str(GROUPS_PATH.relative_to(ROOT)),
        "summary": {
            "icons_total": len(all_icons),
            "grouped": len(grouped),
            "pair_risk": len(pair_risk),
            "isolated": len(isolated),
        },
        "grouped": grouped,
        "pair_risk": pair_risk,
        "isolated": isolated,
    }


def main() -> None:
    coverage = build_coverage()
    OUTPUT_PATH.write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote {OUTPUT_PATH.relative_to(ROOT)} "
        f"for {coverage['summary']['icons_total']} icons."
    )


if __name__ == "__main__":
    main()

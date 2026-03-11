#!/usr/bin/env python3
"""Remove boundary (bnd_en) phrases from train_en.csv for each icon.

Boundary phrases describe a *different* icon but are labeled as the current icon,
making them mislabeled training samples that add noise to the classifier.

Source of truth: icons/*/icon_log.json  →  "boundary" list.
Any text in that list that appears in train_en.csv is removed.

Usage:
    python3 scripts/remove_boundary_from_train.py            # dry-run
    python3 scripts/remove_boundary_from_train.py --apply   # write changes
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to disk. Without this flag, runs in dry-run mode.",
    )
    parser.add_argument(
        "--icons-dir",
        type=Path,
        default=ICONS_DIR,
        help=f"Directory containing icon folders. Default: {ICONS_DIR}",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def process_icon(icon_dir: Path, apply: bool) -> dict[str, object] | None:
    log_path = icon_dir / "icon_log.json"
    train_path = icon_dir / "train_en.csv"

    if not log_path.exists() or not train_path.exists():
        return None

    boundary = set(json.load(log_path.open()).get("boundary", []))
    if not boundary:
        return None

    rows = read_rows(train_path)
    kept = [r for r in rows if r["text"].strip() not in boundary]
    removed = [r["text"].strip() for r in rows if r["text"].strip() in boundary]

    if not removed:
        return None

    if apply:
        write_rows(train_path, kept)

    return {
        "icon": icon_dir.name,
        "removed_count": len(removed),
        "remaining_train_rows": len(kept),
        "removed_phrases": removed,
    }


def main() -> None:
    args = parse_args()
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Mode: {mode}\n")

    results = []
    for icon_dir in sorted(p for p in args.icons_dir.iterdir() if p.is_dir()):
        result = process_icon(icon_dir, args.apply)
        if result:
            results.append(result)

    total_removed = sum(r["removed_count"] for r in results)
    print(f"Icons affected:    {len(results)}")
    print(f"Rows removed:      {total_removed}")
    print(f"")

    for r in results:
        print(f"  {r['icon']} (-{r['removed_count']} rows, {r['remaining_train_rows']} remain)")

    if not args.apply:
        print("\nRun with --apply to write changes.")
    else:
        print("\nDone. Re-run audit_icon_dataset.py to verify.")


if __name__ == "__main__":
    main()

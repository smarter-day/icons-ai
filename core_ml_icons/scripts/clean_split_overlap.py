#!/usr/bin/env python3
"""Remove exact cross-split leakage while preserving EN/RU row alignment."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
SPLITS = ("train", "valid", "test")
LANGS = ("en", "ru")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove exact duplicate texts across train/valid/test for icons that have "
            "aligned English and Russian datasets."
        )
    )
    parser.add_argument(
        "--icons-dir",
        type=Path,
        default=ICONS_DIR,
        help=f"Directory containing icon folders. Default: {ICONS_DIR}",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned removals without rewriting CSV files.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a JSON summary.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header != ["text", "label"]:
            raise ValueError(f"{path} must contain exactly these headers: text,label")
        for raw_row in reader:
            if not raw_row:
                continue
            if len(raw_row) < 2:
                raise ValueError(f"{path} contains an invalid row with fewer than 2 columns: {raw_row}")
            text = ",".join(raw_row[:-1]).strip()
            label = raw_row[-1].strip()
            rows.append({"text": text, "label": label})
    return rows


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["text", "label"])
        writer.writerows((row["text"], row["label"]) for row in rows)


def load_icon(icon_dir: Path) -> dict[str, dict[str, list[dict[str, str]]]] | None:
    loaded: dict[str, dict[str, list[dict[str, str]]]] = {}
    for split in SPLITS:
        loaded[split] = {}
        counts = set()
        for lang in LANGS:
            path = icon_dir / f"{split}_{lang}.csv"
            if not path.exists():
                return None
            rows = read_rows(path)
            loaded[split][lang] = rows
            counts.add(len(rows))
        if len(counts) != 1:
            return None
    return loaded


def build_duplicate_index(rows: list[dict[str, str]]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        index[row["text"].strip()].append(idx)
    return index


def plan_icon_cleanup(icon_dir: Path) -> dict[str, object] | None:
    loaded = load_icon(icon_dir)
    if loaded is None:
        return None

    removals: dict[str, set[int]] = {split: set() for split in SPLITS}

    # Prefer keeping evaluation examples over train. For valid/test overlap, keep valid.
    for lang in LANGS:
        train_index = build_duplicate_index(loaded["train"][lang])
        valid_index = build_duplicate_index(loaded["valid"][lang])
        test_index = build_duplicate_index(loaded["test"][lang])

        for text, indices in train_index.items():
            if text in valid_index or text in test_index:
                removals["train"].update(indices)

        for text, indices in test_index.items():
            if text in valid_index:
                removals["test"].update(indices)

    if not any(removals.values()):
        return None

    summary = {
        "icon": icon_dir.name,
        "removals": {split: sorted(indices) for split, indices in removals.items() if indices},
        "before_counts": {split: len(loaded[split]["en"]) for split in SPLITS},
        "after_counts": {
            split: len(loaded[split]["en"]) - len(indices)
            for split, indices in removals.items()
        },
    }
    return summary


def apply_icon_cleanup(icon_dir: Path, plan: dict[str, object]) -> None:
    removals: dict[str, list[int]] = plan["removals"]  # type: ignore[assignment]
    for split in SPLITS:
        indices = set(removals.get(split, []))
        if not indices:
            continue
        for lang in LANGS:
            path = icon_dir / f"{split}_{lang}.csv"
            rows = read_rows(path)
            filtered = [row for idx, row in enumerate(rows) if idx not in indices]
            write_rows(path, filtered)


def main() -> None:
    args = parse_args()
    planned = []
    skipped = []

    for icon_dir in sorted(path for path in args.icons_dir.iterdir() if path.is_dir()):
        plan = plan_icon_cleanup(icon_dir)
        if plan is None:
            if load_icon(icon_dir) is None:
                skipped.append(icon_dir.name)
            continue
        planned.append(plan)
        if not args.dry_run:
            apply_icon_cleanup(icon_dir, plan)

    summary = {
        "icons_cleaned": len(planned),
        "skipped_icons": skipped,
        "planned": planned,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    print(f"icons_cleaned: {len(planned)}")
    if skipped:
        print(f"skipped_icons: {len(skipped)}")
    for item in planned[:40]:
        print(
            f"{item['icon']}: "
            + ", ".join(
                f"{split} -{len(indices)}"
                for split, indices in item["removals"].items()
            )
        )
    if len(planned) > 40:
        print(f"... and {len(planned) - 40} more")


if __name__ == "__main__":
    main()

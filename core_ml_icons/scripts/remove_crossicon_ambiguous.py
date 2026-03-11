#!/usr/bin/env python3
"""Remove train rows whose text appears in 3+ different icons' datasets.

Such texts (e.g. "fruit", "health", "car") create conflicting labels —
the classifier sees the same input mapped to many different outputs and
cannot learn a useful mapping from it.

By default removes from train_en.csv and train_ru.csv.
Matching for Russian is done by finding which EN texts were removed,
then removing rows at the same positions in the RU file (since EN and RU
are row-aligned). If EN/RU row counts differ, RU is left untouched for
that icon (flagged in output).

Usage:
    python3 scripts/remove_crossicon_ambiguous.py            # dry-run, threshold=3
    python3 scripts/remove_crossicon_ambiguous.py --apply
    python3 scripts/remove_crossicon_ambiguous.py --apply --threshold 5
    python3 scripts/remove_crossicon_ambiguous.py --apply --export-removed removed.json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
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
        "--threshold",
        type=int,
        default=3,
        help="Remove texts that appear in this many or more icons. Default: 3",
    )
    parser.add_argument(
        "--icons-dir",
        type=Path,
        default=ICONS_DIR,
        help=f"Directory containing icon folders. Default: {ICONS_DIR}",
    )
    parser.add_argument(
        "--export-removed",
        type=Path,
        default=None,
        help="Write the list of removed texts and their icon counts to a JSON file.",
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


def collect_train_texts(icons_dir: Path) -> dict[str, set[str]]:
    """Return {text: {icon1, icon2, ...}} from all train_en.csv files."""
    text_to_icons: dict[str, set[str]] = defaultdict(set)
    for icon_dir in (p for p in icons_dir.iterdir() if p.is_dir()):
        path = icon_dir / "train_en.csv"
        if not path.exists():
            continue
        for row in read_rows(path):
            text_to_icons[row["text"].strip()].add(icon_dir.name)
    return text_to_icons


def build_removal_set(text_to_icons: dict[str, set[str]], threshold: int) -> dict[str, set[str]]:
    """Return {text: {icon1, ...}} for texts meeting the threshold."""
    return {text: icons for text, icons in text_to_icons.items() if len(icons) >= threshold}


def process_icon(
    icon_dir: Path,
    removal_set: dict[str, set[str]],
    apply: bool,
) -> dict[str, object] | None:
    en_path = icon_dir / "train_en.csv"
    ru_path = icon_dir / "train_ru.csv"

    if not en_path.exists():
        return None

    en_rows = read_rows(en_path)
    keep_mask = [r["text"].strip() not in removal_set for r in en_rows]
    en_kept = [r for r, keep in zip(en_rows, keep_mask) if keep]
    removed_texts = [r["text"].strip() for r, keep in zip(en_rows, keep_mask) if not keep]

    if not removed_texts:
        return None

    ru_result = "n/a"
    ru_rows_before = 0
    ru_rows_after = 0

    if ru_path.exists():
        ru_rows = read_rows(ru_path)
        ru_rows_before = len(ru_rows)
        if len(ru_rows) == len(en_rows):
            # Row-aligned — apply the same mask
            ru_kept = [r for r, keep in zip(ru_rows, keep_mask) if keep]
            ru_rows_after = len(ru_kept)
            ru_result = "cleaned"
            if apply:
                write_rows(ru_path, ru_kept)
        else:
            ru_result = "skipped (row count mismatch)"
            ru_rows_after = ru_rows_before

    if apply:
        write_rows(en_path, en_kept)

    return {
        "icon": icon_dir.name,
        "en_removed": len(removed_texts),
        "en_remaining": len(en_kept),
        "ru_status": ru_result,
        "ru_before": ru_rows_before,
        "ru_after": ru_rows_after,
        "removed_texts": removed_texts,
    }


def main() -> None:
    args = parse_args()
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Mode: {mode}  |  Threshold: ≥{args.threshold} icons\n")

    text_to_icons = collect_train_texts(args.icons_dir)
    removal_set = build_removal_set(text_to_icons, args.threshold)

    print(f"Unique texts in all train_en files: {len(text_to_icons)}")
    print(f"Texts appearing in ≥{args.threshold} icons: {len(removal_set)}")

    top = sorted(removal_set.items(), key=lambda kv: -len(kv[1]))[:15]
    print("\nTop ambiguous texts:")
    for text, icons in top:
        print(f"  [{len(icons)} icons] {text!r}")
    print()

    results = []
    for icon_dir in sorted(p for p in args.icons_dir.iterdir() if p.is_dir()):
        result = process_icon(icon_dir, removal_set, args.apply)
        if result:
            results.append(result)

    total_en_removed = sum(r["en_removed"] for r in results)
    total_ru_cleaned = sum(1 for r in results if r["ru_status"] == "cleaned")

    print(f"Icons affected:        {len(results)}")
    print(f"EN rows removed:       {total_en_removed}")
    print(f"RU files cleaned:      {total_ru_cleaned}")
    mismatches = [r for r in results if "mismatch" in r["ru_status"]]
    if mismatches:
        print(f"RU row-count mismatches (not cleaned): {len(mismatches)}")
        for r in mismatches:
            print(f"  {r['icon']}: EN {len(r['removed_texts'])} removed, RU {r['ru_before']} rows")

    if args.export_removed:
        export = [
            {"text": text, "icon_count": len(icons), "icons": sorted(icons)}
            for text, icons in sorted(removal_set.items(), key=lambda kv: -len(kv[1]))
        ]
        args.export_removed.write_text(json.dumps(export, ensure_ascii=False, indent=2))
        print(f"\nExported removal list → {args.export_removed}")

    if not args.apply:
        print("\nRun with --apply to write changes.")
    else:
        print("\nDone. Re-run merge_icon_datasets.py and audit_icon_dataset.py to verify.")


if __name__ == "__main__":
    main()

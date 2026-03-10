#!/usr/bin/env python3
"""Merge per-icon CSV datasets from icons/ into one Core ML-ready dataset."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = ROOT / "icons"
DEFAULT_OUTPUT_DIR = ROOT / "merged_icons_dataset"
SPLITS = ("train", "valid", "test")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Collect all icon datasets from icons/<icon>/ and merge them into "
            "3 CSV files for Core ML training."
        )
    )
    parser.add_argument(
        "--lang",
        default="en",
        choices=("en", "ru"),
        help="Dataset language suffix to merge. Default: en",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help=f"Directory with per-icon datasets. Default: {DEFAULT_SOURCE_DIR}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Where merged CSV files will be written. Default: {DEFAULT_OUTPUT_DIR}",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed used for deterministic shuffling. Default: 42",
    )
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="Keep original row order instead of shuffling merged files.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Skip icon folders that do not contain all 3 split files.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"text", "label"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError(f"{path} must contain exactly these headers: text,label")
        return [(row["text"], row["label"]) for row in reader]


def write_rows(path: Path, rows: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["text", "label"])
        writer.writerows(rows)


def collect_icon_dirs(source_dir: Path) -> list[Path]:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    return sorted(path for path in source_dir.iterdir() if path.is_dir())


def merge_datasets(
    source_dir: Path,
    lang: str,
    allow_missing: bool,
) -> tuple[dict[str, list[tuple[str, str]]], list[str], list[dict[str, object]]]:
    merged_rows = {split: [] for split in SPLITS}
    used_icons: list[str] = []
    skipped_icons: list[dict[str, object]] = []
    missing_errors: list[str] = []

    for icon_dir in collect_icon_dirs(source_dir):
        split_paths = {split: icon_dir / f"{split}_{lang}.csv" for split in SPLITS}
        existing_count = sum(path.exists() for path in split_paths.values())

        if existing_count == 0:
            continue

        missing_splits = [split for split, path in split_paths.items() if not path.exists()]
        if missing_splits:
            if allow_missing:
                skipped_icons.append(
                    {
                        "icon": icon_dir.name,
                        "reason": "missing split files",
                        "missing_splits": missing_splits,
                    }
                )
                continue
            missing_files = ", ".join(f"{split}_{lang}.csv" for split in missing_splits)
            missing_errors.append(f"{icon_dir.name}: missing {missing_files}")
            continue

        for split, path in split_paths.items():
            merged_rows[split].extend(read_rows(path))
        used_icons.append(icon_dir.name)

    if missing_errors:
        details = "\n".join(f"  - {message}" for message in missing_errors)
        raise SystemExit(
            "Found icon folders with incomplete datasets.\n"
            "Run again with --allow-missing to skip them.\n"
            f"{details}"
        )

    if not used_icons:
        raise SystemExit(f"No complete *_{lang}.csv datasets were found in {source_dir}.")

    return merged_rows, used_icons, skipped_icons


def shuffle_rows(rows_by_split: dict[str, list[tuple[str, str]]], seed: int) -> None:
    for index, split in enumerate(SPLITS):
        rng = random.Random(seed + index)
        rng.shuffle(rows_by_split[split])


def write_summary(
    output_dir: Path,
    lang: str,
    source_dir: Path,
    used_icons: list[str],
    skipped_icons: list[dict[str, object]],
    rows_by_split: dict[str, list[tuple[str, str]]],
) -> Path:
    summary_path = output_dir / f"merge_summary_{lang}.json"
    summary = {
        "language": lang,
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "icons_merged": len(used_icons),
        "icon_names": used_icons,
        "skipped_icons": skipped_icons,
        "row_counts": {split: len(rows) for split, rows in rows_by_split.items()},
    }
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    return summary_path


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()

    rows_by_split, used_icons, skipped_icons = merge_datasets(
        source_dir=source_dir,
        lang=args.lang,
        allow_missing=args.allow_missing,
    )

    if not args.no_shuffle:
        shuffle_rows(rows_by_split, seed=args.seed)

    output_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    for split in SPLITS:
        output_path = output_dir / f"{split}_{args.lang}.csv"
        write_rows(output_path, rows_by_split[split])
        written_files.append(output_path)

    summary_path = write_summary(
        output_dir=output_dir,
        lang=args.lang,
        source_dir=source_dir,
        used_icons=used_icons,
        skipped_icons=skipped_icons,
        rows_by_split=rows_by_split,
    )

    print(f"Merged {len(used_icons)} icon folders from {source_dir}")
    for split, path in zip(SPLITS, written_files):
        print(f"  {path.name}: {len(rows_by_split[split])} rows")
    print(f"  summary: {summary_path.name}")


if __name__ == "__main__":
    main()

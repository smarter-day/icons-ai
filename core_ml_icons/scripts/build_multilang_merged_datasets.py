#!/usr/bin/env python3
"""Build per-language merged datasets and optional combined CSVs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from merge_icon_datasets import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SOURCE_DIR,
    SPLITS,
    merge_datasets,
    shuffle_rows,
    write_rows,
    write_summary,
)


DEFAULT_LANGS = ("en", "de", "ja", "fr", "es", "ru")
FAMILY_LANGS = {
    "latin": ("en", "de", "fr", "es"),
    "cyrillic": ("ru",),
    "cjk": ("ja",),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Merge all icons for multiple languages and optionally build "
            "train/valid/test combined CSVs."
        )
    )
    parser.add_argument(
        "--langs",
        nargs="+",
        default=None,
        help=(
            "Language suffixes to merge, in the order used for combined CSVs. "
            f"Default when no family is selected: {' '.join(DEFAULT_LANGS)}"
        ),
    )
    parser.add_argument(
        "--families",
        nargs="+",
        choices=sorted(FAMILY_LANGS),
        help=(
            "Build separate merged CSVs for writing-system families. "
            "Available presets: latin, cyrillic, cjk."
        ),
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
        help="Keep original row order inside each language instead of shuffling.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Skip icon folders that do not contain all 3 split files.",
    )
    parser.add_argument(
        "--skip-combined",
        action="store_true",
        help="Only write per-language merged CSVs and summaries.",
    )
    parser.add_argument(
        "--write-language-files",
        action="store_true",
        help="Also write per-language train_<lang>.csv / valid_<lang>.csv / test_<lang>.csv files.",
    )
    return parser.parse_args()


def resolve_langs(args: argparse.Namespace) -> list[str]:
    if args.langs:
        return list(dict.fromkeys(args.langs))

    if args.families:
        langs: list[str] = []
        for family in args.families:
            langs.extend(FAMILY_LANGS[family])
        return list(dict.fromkeys(langs))

    return list(DEFAULT_LANGS)


def write_summary_file(summary_path: Path, summary: dict[str, object]) -> Path:
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, ensure_ascii=False, indent=2)
    return summary_path


def write_combined_summary(
    output_dir: Path,
    langs: list[str],
    rows_by_lang: dict[str, dict[str, list[tuple[str, str]]]],
    icons_by_lang: dict[str, list[str]],
    output_name: str,
    family: str | None = None,
) -> Path:
    summary_path = output_dir / f"merge_summary_{output_name}.json"
    summary = {
        "name": output_name,
        "family": family,
        "languages": langs,
        "output_dir": str(output_dir),
        "row_counts": {
            split: sum(len(rows_by_lang[lang][split]) for lang in langs) for split in SPLITS
        },
        "row_counts_by_language": {
            lang: {split: len(rows_by_lang[lang][split]) for split in SPLITS} for lang in langs
        },
        "icons_merged_by_language": {lang: len(icons_by_lang[lang]) for lang in langs},
    }
    return write_summary_file(summary_path, summary)


def write_grouped_dataset(
    output_dir: Path,
    output_name: str,
    langs: list[str],
    rows_by_lang: dict[str, dict[str, list[tuple[str, str]]]],
    icons_by_lang: dict[str, list[str]],
    family: str | None = None,
) -> Path:
    for split in SPLITS:
        grouped_rows: list[tuple[str, str]] = []
        for lang in langs:
            grouped_rows.extend(rows_by_lang[lang][split])
        write_rows(output_dir / f"{split}_{output_name}.csv", grouped_rows)

    return write_combined_summary(
        output_dir=output_dir,
        langs=langs,
        rows_by_lang=rows_by_lang,
        icons_by_lang=icons_by_lang,
        output_name=output_name,
        family=family,
    )


def main() -> None:
    args = parse_args()
    source_dir = args.source_dir.resolve()
    output_dir = args.output_dir.resolve()
    explicit_langs = args.langs is not None
    langs = resolve_langs(args)

    output_dir.mkdir(parents=True, exist_ok=True)

    rows_by_lang: dict[str, dict[str, list[tuple[str, str]]]] = {}
    icons_by_lang: dict[str, list[str]] = {}

    for lang in langs:
        rows_by_split, used_icons, skipped_icons = merge_datasets(
            source_dir=source_dir,
            lang=lang,
            allow_missing=args.allow_missing,
        )
        if not args.no_shuffle:
            shuffle_rows(rows_by_split, seed=args.seed)

        if args.write_language_files or not args.families:
            for split in SPLITS:
                write_rows(output_dir / f"{split}_{lang}.csv", rows_by_split[split])

            write_summary(
                output_dir=output_dir,
                lang=lang,
                source_dir=source_dir,
                used_icons=used_icons,
                skipped_icons=skipped_icons,
                rows_by_split=rows_by_split,
            )

        rows_by_lang[lang] = rows_by_split
        icons_by_lang[lang] = used_icons

    summary_path: Path | None = None
    build_combined = not args.skip_combined and (explicit_langs or not args.families)
    if build_combined:
        summary_path = write_grouped_dataset(
            output_dir=output_dir,
            output_name="combined",
            langs=langs,
            rows_by_lang=rows_by_lang,
            icons_by_lang=icons_by_lang,
        )

    family_summaries: list[tuple[str, Path]] = []
    for family in args.families or []:
        family_langs = [lang for lang in FAMILY_LANGS[family] if lang in rows_by_lang]
        if not family_langs:
            continue
        family_summary = write_grouped_dataset(
            output_dir=output_dir,
            output_name=family,
            langs=family_langs,
            rows_by_lang=rows_by_lang,
            icons_by_lang=icons_by_lang,
            family=family,
        )
        family_summaries.append((family, family_summary))

    print(f"Built merged datasets for: {', '.join(langs)}")
    if summary_path is not None:
        for split in SPLITS:
            total = sum(len(rows_by_lang[lang][split]) for lang in langs)
            print(f"  {split}_combined.csv: {total} rows")
        print(f"  summary: {summary_path.name}")
    for family, family_summary in family_summaries:
        family_langs = [lang for lang in FAMILY_LANGS[family] if lang in rows_by_lang]
        print(f"  family {family}: {', '.join(family_langs)}")
        for split in SPLITS:
            total = sum(len(rows_by_lang[lang][split]) for lang in family_langs)
            print(f"    {split}_{family}.csv: {total} rows")
        print(f"    summary: {family_summary.name}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit bilingual icon datasets for structure, sync, and common quality issues."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
SPLITS = ("train", "valid", "test")
LANGS = ("en", "ru")
COMMON_AMBIGUOUS_TERMS = {
    "en": {
        "travel",
        "music",
        "tool",
        "holiday",
        "food",
        "building",
        "vehicle",
        "location",
    },
    "ru": {
        "путешествие",
        "музыка",
        "инструмент",
        "праздник",
        "еда",
        "здание",
        "транспорт",
        "локация",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit icon datasets for bilingual structure and editorial quality."
    )
    parser.add_argument(
        "--icons-dir",
        type=Path,
        default=ICONS_DIR,
        help=f"Directory containing icon folders. Default: {ICONS_DIR}",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the full audit report as JSON.",
    )
    parser.add_argument(
        "--min-train",
        type=int,
        default=60,
        help="Minimum recommended train rows per language. Default: 60",
    )
    parser.add_argument(
        "--min-valid-test",
        type=int,
        default=10,
        help="Minimum recommended valid/test rows per language. Default: 10",
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


def find_split_overlap(rows_by_split: dict[str, list[dict[str, str]]]) -> dict[str, list[str]]:
    texts = {
        split: {row["text"].strip() for row in rows}
        for split, rows in rows_by_split.items()
    }
    overlaps = {
        "train_valid": sorted(texts["train"] & texts["valid"]),
        "train_test": sorted(texts["train"] & texts["test"]),
        "valid_test": sorted(texts["valid"] & texts["test"]),
    }
    return {name: rows for name, rows in overlaps.items() if rows}


def audit_icon(icon_dir: Path) -> dict[str, object]:
    report: dict[str, object] = {
        "icon": icon_dir.name,
        "missing_files": [],
        "row_counts": {},
        "sync_mismatches": [],
        "duplicate_rows_within_file": [],
        "split_overlap": {},
        "ambiguous_single_term_rows": [],
    }

    rows_by_lang_split: dict[str, dict[str, list[dict[str, str]]]] = {lang: {} for lang in LANGS}

    for split in SPLITS:
        for lang in LANGS:
            path = icon_dir / f"{split}_{lang}.csv"
            key = f"{split}_{lang}"
            if not path.exists():
                report["missing_files"].append(path.name)
                continue
            rows = read_rows(path)
            rows_by_lang_split[lang][split] = rows
            report["row_counts"][key] = len(rows)

            texts = [row["text"].strip() for row in rows]
            if len(texts) != len(set(texts)):
                report["duplicate_rows_within_file"].append(key)

            for row in rows:
                text = row["text"].strip()
                if text.lower() in COMMON_AMBIGUOUS_TERMS[lang]:
                    report["ambiguous_single_term_rows"].append({"file": key, "text": text})

    for split in SPLITS:
        en_key = f"{split}_en"
        ru_key = f"{split}_ru"
        if en_key in report["row_counts"] and ru_key in report["row_counts"]:
            if report["row_counts"][en_key] != report["row_counts"][ru_key]:
                report["sync_mismatches"].append(
                    {
                        "split": split,
                        "en_rows": report["row_counts"][en_key],
                        "ru_rows": report["row_counts"][ru_key],
                    }
                )

    for lang in LANGS:
        if set(rows_by_lang_split[lang]) == set(SPLITS):
            overlap = find_split_overlap(rows_by_lang_split[lang])
            if overlap:
                report["split_overlap"][lang] = overlap

    return report


def build_report(icons_dir: Path, min_train: int, min_valid_test: int) -> dict[str, object]:
    icon_reports = [audit_icon(path) for path in sorted(icons_dir.iterdir()) if path.is_dir()]

    low_coverage = []
    missing_ru = []
    icons_with_issues = []
    global_texts: dict[str, defaultdict[str, set[str]]] = {
        lang: defaultdict(set) for lang in LANGS
    }

    for icon in icon_reports:
        name = str(icon["icon"])
        counts = icon["row_counts"]

        if icon["missing_files"]:
            if any(name.endswith("_ru.csv") for name in icon["missing_files"]):
                missing_ru.append(name)
            elif any(file.endswith("_ru.csv") for file in icon["missing_files"]):
                missing_ru.append(name)

        for split in SPLITS:
            en_key = f"{split}_en"
            ru_key = f"{split}_ru"
            if split == "train":
                if counts.get(en_key, 0) < min_train or counts.get(ru_key, 0) < min_train:
                    low_coverage.append(
                        {
                            "icon": name,
                            "train_en": counts.get(en_key, 0),
                            "train_ru": counts.get(ru_key, 0),
                        }
                    )
            else:
                if counts.get(en_key, 0) < min_valid_test or counts.get(ru_key, 0) < min_valid_test:
                    low_coverage.append(
                        {
                            "icon": name,
                            en_key: counts.get(en_key, 0),
                            ru_key: counts.get(ru_key, 0),
                        }
                    )

        if (
            icon["missing_files"]
            or icon["sync_mismatches"]
            or icon["duplicate_rows_within_file"]
            or icon["split_overlap"]
            or icon["ambiguous_single_term_rows"]
        ):
            icons_with_issues.append(icon)

        for lang in LANGS:
            for split in SPLITS:
                path = icons_dir / name / f"{split}_{lang}.csv"
                if not path.exists():
                    continue
                for row in read_rows(path):
                    global_texts[lang][row["text"].strip()].add(row["label"].strip())

    shared_across_labels = {}
    for lang in LANGS:
        conflicts = []
        for text, labels in global_texts[lang].items():
            if len(labels) > 1:
                conflicts.append({"text": text, "label_count": len(labels), "labels": sorted(labels)[:10]})
        conflicts.sort(key=lambda item: (-item["label_count"], item["text"]))
        shared_across_labels[lang] = conflicts[:100]

    return {
        "icons_total": len(icon_reports),
        "icons_with_issues": len(icons_with_issues),
        "missing_ru_icons": sorted(set(missing_ru)),
        "low_coverage_icons": low_coverage,
        "shared_texts_across_labels": shared_across_labels,
        "icon_reports": icons_with_issues,
    }


def print_human_report(report: dict[str, object]) -> None:
    print(f"icons_total: {report['icons_total']}")
    print(f"icons_with_issues: {report['icons_with_issues']}")
    print(f"missing_ru_icons: {len(report['missing_ru_icons'])}")
    print(f"low_coverage_entries: {len(report['low_coverage_icons'])}")
    print("")

    missing_ru_icons = report["missing_ru_icons"][:25]
    if missing_ru_icons:
        print("Missing Russian datasets:")
        for icon in missing_ru_icons:
            print(f"  - {icon}")
        if len(report["missing_ru_icons"]) > len(missing_ru_icons):
            print(f"  ... and {len(report['missing_ru_icons']) - len(missing_ru_icons)} more")
        print("")

    low_coverage = report["low_coverage_icons"][:25]
    if low_coverage:
        print("Low coverage samples:")
        for item in low_coverage:
            print(f"  - {json.dumps(item, ensure_ascii=False)}")
        if len(report["low_coverage_icons"]) > len(low_coverage):
            print(f"  ... and {len(report['low_coverage_icons']) - len(low_coverage)} more")
        print("")

    shared_en = report["shared_texts_across_labels"]["en"][:15]
    if shared_en:
        print("Most ambiguous English texts:")
        for item in shared_en:
            print(f"  - {item['text']!r}: {item['label_count']} labels")


def main() -> None:
    args = parse_args()
    report = build_report(args.icons_dir, args.min_train, args.min_valid_test)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human_report(report)


if __name__ == "__main__":
    main()

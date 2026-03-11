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
ALL_LANGS = ("en", "ru", "de", "ja", "fr", "es")
COMMON_AMBIGUOUS_TERMS = {
    "en": {
        "travel", "music", "tool", "holiday", "food", "building", "vehicle", "location",
    },
    "ru": {
        "путешествие", "музыка", "инструмент", "праздник", "еда", "здание", "транспорт", "локация",
    },
    "de": {
        "Reise", "Musik", "Werkzeug", "Feiertag", "Essen", "Gebäude", "Fahrzeug", "Ort",
    },
    "ja": {
        "旅行", "音楽", "道具", "休日", "食べ物", "建物", "乗り物", "場所",
    },
    "fr": {
        "voyage", "musique", "outil", "vacances", "nourriture", "bâtiment", "véhicule", "lieu",
    },
    "es": {
        "viaje", "música", "herramienta", "vacaciones", "comida", "edificio", "vehículo", "lugar",
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
    parser.add_argument(
        "--lang",
        nargs="*",
        default=None,
        help="Languages to audit (e.g. --lang en de ja). Default: all available.",
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


def audit_icon(icon_dir: Path, langs: tuple[str, ...] = ALL_LANGS) -> dict[str, object]:
    report: dict[str, object] = {
        "icon": icon_dir.name,
        "missing_files": [],
        "row_counts": {},
        "sync_mismatches": [],
        "duplicate_rows_within_file": [],
        "split_overlap": {},
        "ambiguous_single_term_rows": [],
    }

    rows_by_lang_split: dict[str, dict[str, list[dict[str, str]]]] = {lang: {} for lang in langs}

    for split in SPLITS:
        for lang in langs:
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
                if lang in COMMON_AMBIGUOUS_TERMS and text.lower() in COMMON_AMBIGUOUS_TERMS[lang]:
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

    for lang in langs:
        if set(rows_by_lang_split[lang]) == set(SPLITS):
            overlap = find_split_overlap(rows_by_lang_split[lang])
            if overlap:
                report["split_overlap"][lang] = overlap

    return report


def build_report(icons_dir: Path, min_train: int, min_valid_test: int, langs: tuple[str, ...] = ALL_LANGS) -> dict[str, object]:
    icon_reports = [audit_icon(path, langs=langs) for path in sorted(icons_dir.iterdir()) if path.is_dir()]

    low_coverage = []
    missing_files_by_lang: dict[str, list[str]] = {lang: [] for lang in langs}
    icons_with_issues = []
    global_texts: dict[str, defaultdict[str, set[str]]] = {
        lang: defaultdict(set) for lang in langs
    }

    for icon in icon_reports:
        name = str(icon["icon"])
        counts = icon["row_counts"]

        if icon["missing_files"]:
            for lang in langs:
                if any(f.endswith(f"_{lang}.csv") for f in icon["missing_files"]):
                    missing_files_by_lang[lang].append(name)

        for split in SPLITS:
            for lang in langs:
                key = f"{split}_{lang}"
                threshold = min_train if split == "train" else min_valid_test
                if counts.get(key, 0) < threshold:
                    low_coverage.append({"icon": name, "file": key, "rows": counts.get(key, 0)})

        if (
            icon["missing_files"]
            or icon["sync_mismatches"]
            or icon["duplicate_rows_within_file"]
            or icon["split_overlap"]
            or icon["ambiguous_single_term_rows"]
        ):
            icons_with_issues.append(icon)

        for lang in langs:
            for split in SPLITS:
                path = icons_dir / name / f"{split}_{lang}.csv"
                if not path.exists():
                    continue
                for row in read_rows(path):
                    global_texts[lang][row["text"].strip()].add(row["label"].strip())

    shared_across_labels = {}
    for lang in langs:
        conflicts = []
        for text, labels in global_texts[lang].items():
            if len(labels) > 1:
                conflicts.append({"text": text, "label_count": len(labels), "labels": sorted(labels)[:10]})
        conflicts.sort(key=lambda item: (-item["label_count"], item["text"]))
        shared_across_labels[lang] = conflicts[:100]

    return {
        "icons_total": len(icon_reports),
        "icons_with_issues": len(icons_with_issues),
        "missing_files_by_lang": {lang: sorted(set(icons)) for lang, icons in missing_files_by_lang.items()},
        "low_coverage_icons": low_coverage,
        "shared_texts_across_labels": shared_across_labels,
        "icon_reports": icons_with_issues,
    }


def print_human_report(report: dict[str, object]) -> None:
    print(f"icons_total: {report['icons_total']}")
    print(f"icons_with_issues: {report['icons_with_issues']}")
    print(f"low_coverage_entries: {len(report['low_coverage_icons'])}")
    print("")

    missing_by_lang = report["missing_files_by_lang"]
    for lang, icons in missing_by_lang.items():
        if icons:
            print(f"Missing {lang.upper()} datasets: {len(icons)} icons")
            for icon in icons[:15]:
                print(f"  - {icon}")
            if len(icons) > 15:
                print(f"  ... and {len(icons) - 15} more")
            print("")

    low_coverage = report["low_coverage_icons"][:25]
    if low_coverage:
        print("Low coverage samples:")
        for item in low_coverage:
            print(f"  - {json.dumps(item, ensure_ascii=False)}")
        if len(report["low_coverage_icons"]) > len(low_coverage):
            print(f"  ... and {len(report['low_coverage_icons']) - len(low_coverage)} more")
        print("")

    for lang, conflicts in report["shared_texts_across_labels"].items():
        top = conflicts[:15]
        if top:
            print(f"Most ambiguous {lang.upper()} texts:")
            for item in top:
                print(f"  - {item['text']!r}: {item['label_count']} labels")


def main() -> None:
    args = parse_args()
    langs = tuple(args.lang) if args.lang else ALL_LANGS
    report = build_report(args.icons_dir, args.min_train, args.min_valid_test, langs=langs)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human_report(report)


if __name__ == "__main__":
    main()

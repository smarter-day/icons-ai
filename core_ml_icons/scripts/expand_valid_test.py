#!/usr/bin/env python3
"""Expand valid/test splits from 3 to 8 rows per icon (5 new phrases each).

For EN: generates 5 natural phrases using icon label + search terms.
For RU: generates 5 natural phrases using first search terms from train_ru.csv.

All new phrases are checked against existing content to avoid duplicates.

Usage:
    python3 scripts/expand_valid_test.py            # dry-run
    python3 scripts/expand_valid_test.py --apply    # write changes
    python3 scripts/expand_valid_test.py --apply --icon anchor  # single icon
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
ICONS_JSON = ROOT / "icons.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="Write changes. Without flag: dry-run.")
    parser.add_argument("--icon", default=None,
                        help="Process only this icon (for testing).")
    parser.add_argument("--min-valid", type=int, default=8,
                        help="Skip icons already at or above this count. Default: 8")
    return parser.parse_args()


def read_texts(path: Path) -> list[str]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [row["text"].strip() for row in csv.DictReader(f)]


def append_rows(path: Path, rows: list[tuple[str, str]]) -> None:
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)


def load_icons_json() -> dict:
    with open(ICONS_JSON) as f:
        raw = json.load(f)
    lookup: dict[str, dict] = {}
    for val in raw.values():
        label = val.get("label", "")
        name = label.lower().replace(" ", "-")
        terms = [
            t for t in val.get("search", {}).get("terms", [])
            if t.isascii() and 2 < len(t) < 30
            and not t[0].isupper()
            and "-" not in t
        ]
        lookup[name] = {"label": label, "terms": terms}
    return lookup


def gen_en_valid(label: str, terms: list[str], existing: set[str]) -> list[str]:
    """Generate 5 natural EN valid phrases."""
    lbl = label.lower()
    # Filter terms that are different from the label (to avoid "anchor anchor")
    t = [x for x in terms if x.lower() != lbl]

    candidates = [
        f"{lbl} icon",
        f"{lbl} symbol",
        f"{t[0]} {lbl}" if t else f"{lbl} icon in app",
        f"icon for {t[0]}" if t else f"{lbl} icon for an app",
        f"{lbl} in a task app",
        f"{t[0]} and {t[1]}" if len(t) > 1 else f"{lbl} icon in my app",
        f"use {lbl} icon for {t[1]}" if len(t) > 1 else f"{lbl} symbol",
        f"{lbl} icon in my app",
        f"what icon shows {lbl}",
        f"{t[1]} icon" if len(t) > 1 else f"{lbl} icon",
    ]
    return _pick(candidates, existing, 5)


def gen_en_test(label: str, terms: list[str], existing: set[str]) -> list[str]:
    """Generate 5 natural EN test phrases."""
    lbl = label.lower()
    t = [x for x in terms if x.lower() != lbl]

    candidates = [
        f"show {lbl}",
        f"{lbl} symbol in an app",
        f"add {lbl} icon",
        f"icon of {lbl}",
        f"{t[0]} {lbl}" if t else f"{lbl} for a task",
        f"{lbl} for a task",
        f"{t[1]}" if len(t) > 1 else f"{lbl}",
        f"icon with {t[0]}" if t else f"{lbl} icon",
        f"{lbl} icon for {t[2]}" if len(t) > 2 else f"{lbl} symbol",
        f"find {lbl} icon",
    ]
    return _pick(candidates, existing, 5)


def gen_ru_valid(icon: str, ru_terms: list[str], existing: set[str]) -> list[str]:
    """Generate 5 natural RU valid phrases from existing train_ru terms."""
    if not ru_terms:
        return []
    t = ru_terms

    candidates = [
        f"иконка {t[0]}",
        f"{t[0]} в приложении",
        f"символ {t[0]}",
        f"{t[1]} в приложении" if len(t) > 1 else f"{t[0]} иконка",
        f"иконка для {t[1]}" if len(t) > 1 else f"значок {t[0]}",
        f"{t[0]} значок",
        f"значок {t[1]}" if len(t) > 1 else f"символ {t[0]}",
        f"{t[2]} иконка" if len(t) > 2 else f"иконка {t[0]}",
        f"найти иконку {t[0]}",
        f"{t[0]} и {t[1]}" if len(t) > 1 else f"{t[0]} в приложении",
    ]
    return _pick(candidates, existing, 5)


def gen_ru_test(icon: str, ru_terms: list[str], existing: set[str]) -> list[str]:
    """Generate 5 natural RU test phrases."""
    if not ru_terms:
        return []
    t = ru_terms

    candidates = [
        f"{t[0]} иконка",
        f"{t[0]} для приложения",
        f"добавить иконку {t[0]}",
        f"показать {t[0]}",
        f"{t[1]}" if len(t) > 1 else f"{t[0]}",
        f"значок {t[0]}",
        f"иконка {t[2]}" if len(t) > 2 else f"{t[0]} символ",
        f"{t[1]} значок" if len(t) > 1 else f"иконка {t[0]}",
        f"использовать иконку {t[0]}",
        f"{t[0]} в задаче",
    ]
    return _pick(candidates, existing, 5)


def _pick(candidates: list[str], existing: set[str], n: int) -> list[str]:
    seen = set(existing)
    result = []
    for c in candidates:
        c = c.strip()
        if c and c.lower() not in {x.lower() for x in seen}:
            result.append(c)
            seen.add(c)
        if len(result) == n:
            break
    return result


def get_ru_terms(icon_dir: Path) -> list[str]:
    """Extract single-word Russian search terms from train_ru.csv (first rows)."""
    path = icon_dir / "train_ru.csv"
    if not path.exists():
        return []
    terms = []
    for row in read_texts(path):
        # Single words are likely search terms (no spaces, not too long)
        if " " not in row and len(row) < 20:
            terms.append(row)
        if len(terms) >= 6:
            break
    return terms


def process_icon(
    icon: str,
    icon_dir: Path,
    icons_lookup: dict,
    apply: bool,
    min_valid: int,
) -> dict | None:
    ve_path = icon_dir / "valid_en.csv"
    te_path = icon_dir / "test_en.csv"
    vr_path = icon_dir / "valid_ru.csv"
    tr_path = icon_dir / "test_ru.csv"

    ve_texts = read_texts(ve_path)
    if len(ve_texts) >= min_valid:
        return None  # already has enough

    te_texts = read_texts(te_path)
    vr_texts = read_texts(vr_path)
    tr_texts = read_texts(tr_path)
    train_en_texts = set(read_texts(icon_dir / "train_en.csv"))

    info = icons_lookup.get(icon, {})
    label = info.get("label", icon.replace("-", " ").title())
    terms = info.get("terms", [])
    ru_terms = get_ru_terms(icon_dir)

    # Existing content to avoid duplicating
    all_en_existing = set(ve_texts) | set(te_texts) | train_en_texts
    all_ru_existing = set(vr_texts) | set(tr_texts)

    new_ve = gen_en_valid(label, terms, all_en_existing)
    all_en_existing |= set(new_ve)
    new_te = gen_en_test(label, terms, all_en_existing)

    new_vr = gen_ru_valid(icon, ru_terms, all_ru_existing)
    all_ru_existing |= set(new_vr)
    new_tr = gen_ru_test(icon, ru_terms, all_ru_existing)

    if apply:
        if new_ve and ve_path.exists():
            append_rows(ve_path, [(t, icon) for t in new_ve])
        if new_te and te_path.exists():
            append_rows(te_path, [(t, icon) for t in new_te])
        if new_vr and vr_path.exists():
            append_rows(vr_path, [(t, icon) for t in new_vr])
        if new_tr and tr_path.exists():
            append_rows(tr_path, [(t, icon) for t in new_tr])

    return {
        "icon": icon,
        "new_valid_en": new_ve,
        "new_test_en": new_te,
        "new_valid_ru": new_vr,
        "new_test_ru": new_tr,
        "ru_missing": not ru_terms,
    }


def main() -> None:
    args = parse_args()
    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"Mode: {mode}  |  min-valid threshold: {args.min_valid}\n")

    icons_lookup = load_icons_json()

    if args.icon:
        icon_dirs = [ICONS_DIR / args.icon]
    else:
        icon_dirs = sorted(p for p in ICONS_DIR.iterdir() if p.is_dir())

    results = []
    skipped = 0
    ru_missing = []

    for icon_dir in icon_dirs:
        icon = icon_dir.name
        result = process_icon(icon, icon_dir, icons_lookup, args.apply, args.min_valid)
        if result is None:
            skipped += 1
        else:
            results.append(result)
            if result["ru_missing"]:
                ru_missing.append(icon)

    total_en_valid = sum(len(r["new_valid_en"]) for r in results)
    total_en_test = sum(len(r["new_test_en"]) for r in results)
    total_ru_valid = sum(len(r["new_valid_ru"]) for r in results)
    total_ru_test = sum(len(r["new_test_ru"]) for r in results)

    print(f"Icons processed:    {len(results)}")
    print(f"Icons skipped (≥{args.min_valid} rows): {skipped}")
    print(f"New valid_en rows:  {total_en_valid}")
    print(f"New test_en rows:   {total_en_test}")
    print(f"New valid_ru rows:  {total_ru_valid}")
    print(f"New test_ru rows:   {total_ru_test}")
    print(f"Total new rows:     {total_en_valid + total_en_test + total_ru_valid + total_ru_test}")

    if ru_missing:
        print(f"\nIcons with no RU terms found ({len(ru_missing)}): {ru_missing[:10]}")

    if args.icon and results:
        r = results[0]
        print(f"\nSample — {r['icon']}:")
        print(f"  valid_en: {r['new_valid_en']}")
        print(f"  test_en:  {r['new_test_en']}")
        print(f"  valid_ru: {r['new_valid_ru']}")
        print(f"  test_ru:  {r['new_test_ru']}")

    if not args.apply:
        print("\nRun with --apply to write changes.")
    else:
        print("\nDone. Run merge_icon_datasets.py to rebuild merged CSVs.")


if __name__ == "__main__":
    main()

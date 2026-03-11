#!/usr/bin/env python3
"""Remove developer-speak phrases from train EN and RU files.

Dry-run by default. Pass --apply to write changes.
"""
import argparse, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"

BAD_EN = [
    re.compile(r"I need a .+ icon for", re.I),
    re.compile(r"add a .+ (symbol|icon) to", re.I),
    re.compile(r"show a .+ for the", re.I),
    re.compile(r"use the .+ icon for", re.I),
    re.compile(r"^icon for (the |an |a )", re.I),
]
BAD_RU = [
    re.compile(r"нужна иконка .+ для", re.I),
    re.compile(r"добавить символ .+ в", re.I),
    re.compile(r"показать .+ для .*(категори|раздел|функци|экран)", re.I),
    re.compile(r"использовать иконку .+ для", re.I),
    re.compile(r"мне нужна иконка", re.I),
    re.compile(r"нужен значок .+ для", re.I),
    re.compile(r"добавь символ", re.I),
    re.compile(r"покажи .+ для", re.I),
    re.compile(r"используй иконку", re.I),
]

def is_bad(text, patterns):
    return any(p.search(text) for p in patterns)

def process(path, patterns, apply):
    if not path.exists():
        return 0, 0
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    kept = [r for r in rows if not is_bad(r["text"], patterns)]
    removed = len(rows) - len(kept)
    if removed and apply:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["text", "label"])
            w.writeheader()
            w.writerows(kept)
    return removed, len(kept)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    total_en = total_ru = 0
    for d in sorted(p for p in ICONS_DIR.iterdir() if p.is_dir()):
        rem_en, _ = process(d / "train_en.csv", BAD_EN, args.apply)
        rem_ru, _ = process(d / "train_ru.csv", BAD_RU, args.apply)
        if rem_en or rem_ru:
            print(f"  {d.name}: -EN:{rem_en} -RU:{rem_ru}")
        total_en += rem_en
        total_ru += rem_ru

    print(f"\nTotal removed: EN={total_en} RU={total_ru}")
    if not args.apply:
        print("Dry-run. Pass --apply to write.")

if __name__ == "__main__":
    main()

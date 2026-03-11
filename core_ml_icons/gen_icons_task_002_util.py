#!/usr/bin/env python3
"""Shared utilities for gen_icons_task_002 scripts."""

import csv
import re
from pathlib import Path

icons_dir = Path(__file__).resolve().parent / "icons"

BAD_EN = [
    re.compile(r"add a .+ (symbol|icon|section) to", re.I),
    re.compile(r"add .+ to the .+ section", re.I),
    re.compile(r"show .+ for the .+ feature", re.I),
    re.compile(r"I need a .+ icon for", re.I),
    re.compile(r"use the .+ icon for", re.I),
    re.compile(r"^icon for (the |an |a )", re.I),
    re.compile(r"icon (for|in) a .+ app\b", re.I),
    re.compile(r"icon (representing|shaped)", re.I),
    re.compile(r"emoji for .+ apps", re.I),
    re.compile(r"\bemoji$", re.I),
]
BAD_RU = [
    re.compile(r"добавить символ .+ в", re.I),
    re.compile(r"добавь .+ в раздел", re.I),
    re.compile(r"показать .+ для .*(категори|раздел|функци|экран)", re.I),
    re.compile(r"иконка .+ для .*(приложени|платформ|сервис)", re.I),
    re.compile(r"использовать иконку .+ для", re.I),
    re.compile(r"покажи .+ для", re.I),
    re.compile(r"используй иконку", re.I),
    re.compile(r"эмодзи .+ для .+ приложений", re.I),
    re.compile(r"иконка .+ символизирует", re.I),
    re.compile(r"иконка .+ как символ", re.I),
]


def is_bad(text, patterns):
    return any(p.search(text) for p in patterns)


def read_csv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [(r["text"].strip(), r["label"].strip()) for r in csv.DictReader(f)]


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        w.writerows(rows)


def clean_and_expand(icon, new_en, new_ru, new_de, new_ja, new_fr, new_es,
                     remove_en_texts=None, remove_ru_texts=None):
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"

    existing_en = read_csv(en_path)
    existing_ru = read_csv(ru_path)

    clean_en = [(t, l) for t, l in existing_en if not is_bad(t, BAD_EN)]
    clean_ru = [(t, l) for t, l in existing_ru if not is_bad(t, BAD_RU)]

    if remove_en_texts:
        s = set(remove_en_texts)
        clean_en = [(t, l) for t, l in clean_en if t not in s]
    if remove_ru_texts:
        s = set(remove_ru_texts)
        clean_ru = [(t, l) for t, l in clean_ru if t not in s]

    # Deduplicate
    seen = set()
    dedup = []
    for t, l in clean_en:
        if t not in seen:
            seen.add(t)
            dedup.append((t, l))
    clean_en = dedup

    seen = set()
    dedup = []
    for t, l in clean_ru:
        if t not in seen:
            seen.add(t)
            dedup.append((t, l))
    clean_ru = dedup

    # Append new (skip duplicates)
    en_texts = {t for t, _ in clean_en}
    for t in new_en:
        if t not in en_texts:
            clean_en.append((t, icon))
            en_texts.add(t)

    ru_texts = {t for t, _ in clean_ru}
    for t in new_ru:
        if t not in ru_texts:
            clean_ru.append((t, icon))
            ru_texts.add(t)

    clean_en = clean_en[:60]
    clean_ru = clean_ru[:60]

    write_csv(en_path, clean_en)
    write_csv(ru_path, clean_ru)

    for lang, phrases in [("de", new_de), ("ja", new_ja), ("fr", new_fr), ("es", new_es)]:
        p = icons_dir / icon / f"train_{lang}.csv"
        rows = [(t, icon) for t in phrases[:60]]
        write_csv(p, rows)

    counts = {
        "en": len(clean_en), "ru": len(clean_ru),
        "de": min(len(new_de), 60), "ja": min(len(new_ja), 60),
        "fr": min(len(new_fr), 60), "es": min(len(new_es), 60),
    }
    ok = all(v == 60 for v in counts.values())
    status = "OK" if ok else f"MISMATCH {counts}"
    print(f"  {icon}: {status}")
    return ok

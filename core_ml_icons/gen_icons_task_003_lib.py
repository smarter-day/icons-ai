#!/usr/bin/env python3
"""Shared utilities for task-003 icon generation."""

import csv
from pathlib import Path

icons_dir = Path("icons")


def write_csv(path, rows, label):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        for t in rows:
            w.writerow([t, label])


def build_icon(icon, keep_en, keep_ru, new_en, new_ru, de, ja, fr, es):
    """Clean existing, merge with new, write all 6 langs at exactly 60."""
    all_en = list(dict.fromkeys(keep_en + new_en))
    assert len(all_en) == 60, f"{icon} EN has {len(all_en)}, need 60"
    write_csv(icons_dir / icon / "train_en.csv", all_en, icon)

    all_ru = list(dict.fromkeys(keep_ru + new_ru))
    assert len(all_ru) == 60, f"{icon} RU has {len(all_ru)}, need 60"
    write_csv(icons_dir / icon / "train_ru.csv", all_ru, icon)

    assert len(de) == 60, f"{icon} DE has {len(de)}, need 60"
    write_csv(icons_dir / icon / "train_de.csv", de, icon)

    assert len(ja) == 60, f"{icon} JA has {len(ja)}, need 60"
    write_csv(icons_dir / icon / "train_ja.csv", ja, icon)

    assert len(fr) == 60, f"{icon} FR has {len(fr)}, need 60"
    write_csv(icons_dir / icon / "train_fr.csv", fr, icon)

    assert len(es) == 60, f"{icon} ES has {len(es)}, need 60"
    write_csv(icons_dir / icon / "train_es.csv", es, icon)

    print(f"  {icon}: 60 x 6 langs written")

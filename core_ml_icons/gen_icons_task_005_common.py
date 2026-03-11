#!/usr/bin/env python3
"""Shared utilities for task-005 icon generation."""

import csv
from pathlib import Path

ICONS_DIR = Path(__file__).resolve().parent / "icons"


def write_csv(path, label, texts):
    """Write a complete CSV with header + rows."""
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        for t in texts:
            w.writerow([t, label])


def gen(icon, en, ru, de, ja, fr, es):
    for lang, phrases in [("en", en), ("ru", ru), ("de", de),
                          ("ja", ja), ("fr", fr), ("es", es)]:
        assert len(phrases) == 60, f"{icon}/{lang}: got {len(phrases)}, need 60"
        seen = set()
        for t in phrases:
            low = t.strip().lower()
            assert low not in seen, f"{icon}/{lang}: duplicate: {t}"
            seen.add(low)
        path = ICONS_DIR / icon / f"train_{lang}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        write_csv(path, icon, phrases)
        print(f"  {icon}/train_{lang}.csv: {len(phrases)} rows")

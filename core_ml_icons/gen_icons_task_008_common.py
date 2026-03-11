#!/usr/bin/env python3
"""Shared utilities for task-008 icon generation."""

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
        # check no duplicates
        dupes = [t for t in phrases if phrases.count(t) > 1]
        assert not dupes, f"{icon}/{lang}: duplicates found: {set(dupes)}"
        path = ICONS_DIR / icon / f"train_{lang}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        write_csv(path, icon, phrases)
        print(f"  {icon}/train_{lang}.csv: {len(phrases)} rows")

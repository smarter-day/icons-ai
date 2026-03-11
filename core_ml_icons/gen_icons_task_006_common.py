"""Common helpers for task-003 icon generation."""

import csv
from pathlib import Path

ICONS_DIR = Path(__file__).parent / "icons"
LANGS = ["en", "ru", "de", "ja", "fr", "es"]


def write_csv(path, label, texts):
    """Write a complete train CSV with header + rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        for t in texts:
            w.writerow([t, label])


def build_icon(icon, langs_data):
    """Write all 6 language files for one icon. Verify counts."""
    for lang in LANGS:
        texts = langs_data[lang]
        n = len(texts)
        u = len(set(texts))
        if n != 60:
            print(f"  ERROR {icon}/{lang}: got {n}, expected 60")
            return False
        if u != 60:
            dupes = [t for t in texts if texts.count(t) > 1]
            print(f"  ERROR {icon}/{lang}: {n - u} duplicates: {set(dupes)}")
            return False
        path = ICONS_DIR / icon / f"train_{lang}.csv"
        write_csv(path, icon, texts)
    print(f"  {icon}: OK (60 x 6)")
    return True

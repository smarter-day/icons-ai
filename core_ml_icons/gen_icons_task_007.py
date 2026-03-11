#!/usr/bin/env python3
"""Task-007 runner: snowman, socks, speaker, spider, squirrel,
   steak, stocking, stomach, store, subtitles

Run all parts and verify final counts.
"""
import csv
from pathlib import Path

ICONS_DIR = Path(__file__).parent / "icons"
LANGS = ["en", "ru", "de", "ja", "fr", "es"]
ICONS = [
    "snowman", "socks", "speaker", "spider", "squirrel",
    "steak", "stocking", "stomach", "store", "subtitles",
]

print("=== Running part A (snowman, socks, speaker) ===")
exec(open("gen_icons_task_007a.py").read())

print("\n=== Running part B (spider, squirrel, steak, stocking) ===")
exec(open("gen_icons_task_007b.py").read())

print("\n=== Running part C (stomach, store, subtitles) ===")
exec(open("gen_icons_task_007c.py").read())

print("\n=== Final verification ===")
ok = True
for icon in ICONS:
    for lang in LANGS:
        path = ICONS_DIR / icon / f"train_{lang}.csv"
        if not path.exists():
            print(f"  MISSING: {path}")
            ok = False
            continue
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        n = len(rows)
        texts = [r["text"] for r in rows]
        u = len(set(texts))
        labels = set(r["label"] for r in rows)
        issues = []
        if n != 60:
            issues.append(f"count={n}")
        if u != n:
            issues.append(f"dupes={n - u}")
        if labels != {icon}:
            issues.append(f"bad labels={labels}")
        if issues:
            print(f"  FAIL {icon}/{lang}: {', '.join(issues)}")
            ok = False

if ok:
    print("  ALL 10 icons x 6 langs x 60 rows = OK")
else:
    print("  SOME CHECKS FAILED -- see above")

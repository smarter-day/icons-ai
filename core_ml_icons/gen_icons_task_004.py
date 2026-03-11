#!/usr/bin/env python3
"""Task-004 runner: money-check, monkey, moon, mortar-pestle, mosque,
       mountain, mouse-field, mp3-player, music, mustache
10 icons x 60 phrases x 6 languages.
"""
import subprocess, sys, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

parts = [
    "gen_icons_task_003_part1.py",
    "gen_icons_task_003_part2.py",
    "gen_icons_task_003_part3.py",
    "gen_icons_task_003_part4.py",
    "gen_icons_task_003_part5.py",
]

for p in parts:
    print(f"\n=== Running {p} ===")
    r = subprocess.run([sys.executable, p], capture_output=True, text=True)
    print(r.stdout, end="")
    if r.returncode != 0:
        print(f"FAILED:\n{r.stderr}", file=sys.stderr)
        sys.exit(1)

# ── Verification ─────────────────────────────────────────────────────────────
import csv
from pathlib import Path

icons = [
    "money-check", "monkey", "moon", "mortar-pestle", "mosque",
    "mountain", "mouse-field", "mp3-player", "music", "mustache",
]
langs = ["en", "ru", "de", "ja", "fr", "es"]
icons_dir = Path("icons")

print("\n=== Verification ===")
all_ok = True
for icon in icons:
    for lang in langs:
        p = icons_dir / icon / f"train_{lang}.csv"
        if not p.exists():
            print(f"  MISSING: {p}")
            all_ok = False
            continue
        with p.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        n = len(rows)
        texts = [r["text"] for r in rows]
        dupes = len(texts) - len(set(texts))
        if n != 60 or dupes > 0:
            print(f"  {icon}/{lang}: {n} rows, {dupes} duplicates  {'FAIL' if n != 60 else 'WARN'}")
            if n != 60:
                all_ok = False
        bad_labels = [r for r in rows if r["label"] != icon]
        if bad_labels:
            print(f"  {icon}/{lang}: {len(bad_labels)} wrong labels  FAIL")
            all_ok = False

if all_ok:
    print("  ALL OK: 10 icons x 6 langs x 60 rows each")
else:
    print("  ERRORS FOUND - see above")
    sys.exit(1)

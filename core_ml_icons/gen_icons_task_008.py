#!/usr/bin/env python3
"""Task-008: Generate 60 phrases x 6 languages for 10 icons.

Icons: faucet, ferris-wheel, film, film-canister, fingerprint,
       fire, flag-checkered, flask, floppy-disk, flower

Run:  python gen_icons_task_008.py
"""

import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

scripts = [
    "gen_icons_task_004_part1.py",
    "gen_icons_task_004_part2.py",
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"Running {script}")
    print('='*60)
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(result.stdout, end="")
    if result.returncode != 0:
        print(f"FAILED:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

# Verify all icons have exactly 60 rows in all 6 languages
print(f"\n{'='*60}")
print("Verification")
print('='*60)

import csv
from pathlib import Path

icons_dir = Path("icons")
icons = ["faucet", "ferris-wheel", "film", "film-canister", "fingerprint",
         "fire", "flag-checkered", "flask", "floppy-disk", "flower"]
langs = ["en", "ru", "de", "ja", "fr", "es"]

all_ok = True
for icon in icons:
    for lang in langs:
        path = icons_dir / icon / f"train_{lang}.csv"
        if not path.exists():
            print(f"  MISSING: {icon}/train_{lang}.csv")
            all_ok = False
            continue
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        count = len(rows)
        if count != 60:
            print(f"  WRONG COUNT: {icon}/train_{lang}.csv has {count} rows (need 60)")
            all_ok = False
        # check for duplicates
        texts = [r["text"] for r in rows]
        dupes = set(t for t in texts if texts.count(t) > 1)
        if dupes:
            print(f"  DUPLICATES in {icon}/train_{lang}.csv: {dupes}")
            all_ok = False
        # check label
        bad_labels = [r for r in rows if r["label"] != icon]
        if bad_labels:
            print(f"  BAD LABEL in {icon}/train_{lang}.csv: {len(bad_labels)} rows")
            all_ok = False

if all_ok:
    print("\nAll 10 icons x 6 languages x 60 phrases verified OK!")
else:
    print("\nSome checks FAILED - see above.")
    sys.exit(1)

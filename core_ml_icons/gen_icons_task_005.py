#!/usr/bin/env python3
"""Task-005 runner: Generate 60 phrases x 6 languages for 10 icons.

Icons: plane, plug, popcorn, popsicle, power-off,
       projector, pumpkin, rabbit, raccoon, radiation
"""
import subprocess, sys, csv
from pathlib import Path

parts = [
    "gen_icons_task_005_part1.py",
    "gen_icons_task_005_part2.py",
    "gen_icons_task_005_part3.py",
    "gen_icons_task_005_part4.py",
]

root = Path(__file__).resolve().parent

for p in parts:
    print(f"\n>>> Running {p}")
    r = subprocess.run([sys.executable, str(root / p)], cwd=str(root))
    if r.returncode != 0:
        print(f"FAILED: {p}")
        sys.exit(1)

# ── Verification ──────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("VERIFICATION")
print("="*60)

icons = ["plane", "plug", "popcorn", "popsicle", "power-off",
         "projector", "pumpkin", "rabbit", "raccoon", "radiation"]
langs = ["en", "ru", "de", "ja", "fr", "es"]
all_ok = True

for icon in icons:
    for lang in langs:
        path = root / "icons" / icon / f"train_{lang}.csv"
        if not path.exists():
            print(f"  MISSING: {icon}/train_{lang}.csv")
            all_ok = False
            continue
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        n = len(rows)
        if n != 60:
            print(f"  WRONG COUNT: {icon}/train_{lang}.csv has {n} rows (need 60)")
            all_ok = False
        else:
            # check for duplicates
            texts = [r["text"] for r in rows]
            if len(set(t.lower() for t in texts)) != 60:
                print(f"  DUPLICATES: {icon}/train_{lang}.csv")
                all_ok = False

if all_ok:
    print("\nAll 10 icons x 6 languages x 60 phrases = OK")
else:
    print("\nSome issues found above.")
    sys.exit(1)

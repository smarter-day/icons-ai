#!/usr/bin/env python3
"""Task-006 runner: Generate 60 phrases x 6 languages for 10 icons.

Icons: pen, pencil, people, person-hiking, person-meditating,
       person-walking, phone, piano, pickaxe, pig
"""

import subprocess, sys, csv
from pathlib import Path

ICONS = [
    "pen", "pencil", "people", "person-hiking", "person-meditating",
    "person-walking", "phone", "piano", "pickaxe", "pig",
]
LANGS = ["en", "ru", "de", "ja", "fr", "es"]
ICONS_DIR = Path(__file__).parent / "icons"

# Run each part
for part in ["gen_icons_task_006a", "gen_icons_task_006b", "gen_icons_task_006c"]:
    print(f"\n=== Running {part} ===")
    result = subprocess.run([sys.executable, f"{part}.py"], capture_output=True, text=True,
                           cwd=Path(__file__).parent)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print(f"FAILED: {part}")
        sys.exit(1)

# Verify all files
print("\n=== Verification ===")
all_ok = True
for icon in ICONS:
    for lang in LANGS:
        path = ICONS_DIR / icon / f"train_{lang}.csv"
        if not path.exists():
            print(f"  MISSING: {path}")
            all_ok = False
            continue
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        texts = [r["text"].strip() for r in rows]
        n = len(texts)
        u = len(set(texts))
        if n != 60:
            print(f"  WRONG COUNT {icon}/{lang}: {n} (expected 60)")
            all_ok = False
        elif u != 60:
            dupes = [t for t in texts if texts.count(t) > 1]
            print(f"  DUPLICATES {icon}/{lang}: {n - u} dupes: {set(dupes)}")
            all_ok = False

if all_ok:
    print("  ALL OK: 10 icons x 6 languages x 60 phrases each")
else:
    print("  ERRORS FOUND - see above")
    sys.exit(1)

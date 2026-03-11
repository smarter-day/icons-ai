# Icon Dataset Improvement Plan
**Project:** core_ml_icons / Smarter Day icon search
**Date:** 2026-03-11
**Goal:** Shift training data from "icon description" style to "task manager user input" style

---

## Context

The Core ML model is a 711-class text classifier. When a user types a task name in the
Smarter Day app, the model suggests a matching icon. This means every training phrase
must sound like what a real user would type as a task title — not like a designer
describing an icon.

**Current dataset state:**
- 711 icons total
- Avg EN rows per icon: 36.9
- Icons with < 30 EN rows: 141
- Icons with 30–49 EN rows: 521
- Icons with 50+ EN rows: 49
- ~8% of EN rows (~2,114) are developer-speak ("I need a pepper icon for my recipe app")
- ~4% of RU rows (~1,191) are developer-speak equivalents
- Many `reg` category phrases are visual icon descriptions, not task titles

**Working directory:** `/Users/idjugostran/Projects/icons-ai/core_ml_icons/`

**Key files:**
```
icons/                          — one subdirectory per icon
  {icon}/train_en.csv           — text,label
  {icon}/train_ru.csv
  {icon}/valid_en.csv
  {icon}/test_en.csv
  {icon}/valid_ru.csv
  {icon}/test_ru.csv
  {icon}/icon_log.json
merged_icons_dataset/           — rebuilt by merge_icon_datasets.py
scripts/audit_icon_dataset.py   — run after every change to verify
scripts/merge_icon_datasets.py  — merge: python3 scripts/merge_icon_datasets.py --lang en --allow-missing
docs/icon-dataset-editorial-guide.md
```

---

## The Core Problem

Current phrase categories (from the original gen_icons template) do NOT match user input:

| Category | Example (pepper) | Useful? |
|----------|-----------------|---------|
| search term | `bell pepper` | ✅ users type keywords |
| visual description | `bright red pepper with a green stem on top` | ❌ nobody types this as a task |
| developer-speak | `I need a pepper icon for my recipe app` | ❌ task manager user would never type this |
| task-like | `buy bell peppers at the grocery store` | ✅ this is what we need |
| typo | `pepepr chopped for stir fry` | ✅ realistic noise |
| boundary | describes a *different* similar icon | ✅ critical for precision |

---

## New Phrase Template (Task-First)

All new phrases must follow this template. Use it for every icon going forward.

### EN phrase categories (target: 60 rows per icon)

**1. Keyword / search term (3–5 rows)**
Short words a user types when searching fast. Include the icon's canonical name and close synonyms.
```
bell pepper
capsicum
pepper vegetable
```

**2. Direct task title — action verb (8–10 rows)**
User creates a task with a clear action. Should feel like a real to-do item.
```
buy bell peppers for the week
slice peppers for the stir fry
roast the peppers in the oven
stuff the peppers with rice and meat
add peppers to the grocery list
```

**3. Contextual task — with time or purpose (6–8 rows)**
Task with a when/why/where that makes it more specific.
```
peppers for Sunday dinner
don't forget peppers for the taco night
pick up peppers before the store closes
peppers for the meal prep this weekend
```

**4. Short informal / power-user style (4–5 rows)**
How people type when in a hurry. Fragment-like, natural.
```
need peppers
grab peppers
peppers - grocery run
peppers tonight
```

**5. Conversational / natural language (4–5 rows)**
Slightly longer, reads like real spoken thought typed quickly.
```
we're out of peppers — need to buy some
peppers are on sale at the supermarket this week
remember to get peppers for the recipe
```

**6. Realistic typos (4 rows)**
Adjacent-key or missing-letter mistakes only. Must still be recognisable.
```
pepepr sliced for stir fry
bel pepper from the store
papper for the salad
capsicm in the grocery list
```

**7. Boundary phrases — describe a DIFFERENT similar icon (5–6 rows)**
CRITICAL: These must describe a neighbouring icon, NOT the current one.
For pepper the boundary icon could be: chili, avocado, tomato, carrot.
Write natural phrases that describe THOSE icons as if someone typed a task.
```
pick up a ripe avocado for the guacamole        ← avocado icon
add chili peppers to the hot sauce order         ← chili icon
slice a tomato for the bruschetta                ← tomato icon
```

### RU phrase categories (same structure, same count)

Follow the same 7 categories. Every RU phrase must have a corresponding EN intent.
Do NOT machine-translate directly — write naturally in Russian.

```
# keyword
болгарский перец
капсикум
перец овощ

# direct task
купить болгарский перец на неделю
нарезать перец для стир-фрая
запечь перцы в духовке
нафаршировать перцы рисом и мясом
добавить перец в список покупок

# contextual
перцы для воскресного ужина
не забыть перец для тако-вечера
купить перцы до закрытия магазина
перцы для готовки на выходных

# short informal
нужны перцы
взять перцы
перцы — список покупок
перцы сегодня

# conversational
перцы закончились — надо купить
перцы продаются со скидкой в этом магазине
не забудь перцы для рецепта

# typos
перец нарблен для стир-фрая
болгарскй перец из магазина
паприка для салата
перцы из списка

# boundary (avocado, chili, tomato)
спелый авокадо для гуакамоле
добавить чили-перцы в заказ соуса
нарезать помидор для брускетты
```

---

## What Must Be Removed from Existing Data

### Patterns to delete (automated)

**EN — developer-speak (regex patterns):**
```
I need a .+ icon for
add a .+ (symbol|icon) to
show a .+ for the
use the .+ icon for
icon for (the |an |a )
```

**RU — developer-speak:**
```
нужна иконка .+ для
добавить символ .+ в
показать .+ для .* (категории|раздела|функции|экрана)
использовать иконку .+ для
мне нужна иконка
нужен значок .+ для
добавь символ
покажи .+ для
используй иконку
```

**Visual descriptions (manual review, icon by icon):**
Phrases like "bright red X with a green stem" or "circular icon showing Y" — these are
not wrong enough to auto-delete but should be replaced when touching an icon.

---

## Execution Steps

### Step 1 — Remove developer-speak rows (automated)

Write `scripts/remove_devspeak.py`:

```python
#!/usr/bin/env python3
"""Remove developer-speak phrases from train EN and RU files.

Dry-run by default. Pass --apply to write changes.
"""
import argparse, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"

BAD_EN = [
    re.compile(r"I need a .+ icon for", re.I),
    re.compile(r"add a .+ (symbol|icon) to", re.I),
    re.compile(r"show a .+ for the", re.I),
    re.compile(r"use the .+ icon for", re.I),
    re.compile(r"^icon for (the |an |a )", re.I),
]
BAD_RU = [
    re.compile(r"нужна иконка .+ для", re.I),
    re.compile(r"добавить символ .+ в", re.I),
    re.compile(r"показать .+ для .*(категори|раздел|функци|экран)", re.I),
    re.compile(r"использовать иконку .+ для", re.I),
    re.compile(r"мне нужна иконка", re.I),
    re.compile(r"нужен значок .+ для", re.I),
    re.compile(r"добавь символ", re.I),
    re.compile(r"покажи .+ для", re.I),
    re.compile(r"используй иконку", re.I),
]

def is_bad(text, patterns):
    return any(p.search(text) for p in patterns)

def process(path, patterns, apply):
    if not path.exists():
        return 0, 0
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    kept = [r for r in rows if not is_bad(r["text"], patterns)]
    removed = len(rows) - len(kept)
    if removed and apply:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["text", "label"])
            w.writeheader()
            w.writerows(kept)
    return removed, len(kept)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    total_en = total_ru = 0
    for d in sorted(p for p in ICONS_DIR.iterdir() if p.is_dir()):
        rem_en, _ = process(d / "train_en.csv", BAD_EN, args.apply)
        rem_ru, _ = process(d / "train_ru.csv", BAD_RU, args.apply)
        if rem_en or rem_ru:
            print(f"  {d.name}: -EN:{rem_en} -RU:{rem_ru}")
        total_en += rem_en
        total_ru += rem_ru

    print(f"\nTotal removed: EN={total_en} RU={total_ru}")
    if not args.apply:
        print("Dry-run. Pass --apply to write.")

if __name__ == "__main__":
    main()
```

**Run:**
```bash
python3 scripts/remove_devspeak.py           # dry-run first
python3 scripts/remove_devspeak.py --apply   # then apply
```

---

### Step 2 — Add task-style phrases to all icons below 60 rows

Process icons in batches of 20, lowest coverage first.

**For each icon:**
1. Read `train_en.csv` and `train_ru.csv` — understand what's already there
2. Check `icon_log.json` for search terms and boundary icon hints
3. Write 20–35 new EN phrases following the new template
4. Write the matching 20–35 RU phrases (same intent, natural Russian)
5. Append to CSV files (never overwrite the whole file)

**Priority order (lowest EN rows first):**
```bash
python3 - <<'EOF'
import csv
from pathlib import Path
stats = []
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    f = d / "train_en.csv"
    if not f.exists(): continue
    with f.open() as fp:
        rows = sum(1 for _ in csv.DictReader(fp))
    if rows < 60:
        stats.append((rows, d.name))
stats.sort()
for r, n in stats:
    print(f"{n}: {r}")
EOF
```

**Append helper (use in every batch script):**
```python
import csv
from pathlib import Path

icons_dir = Path("icons")

def read_texts(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r["text"].strip() for r in csv.DictReader(f)]

def append_csv(path, rows):
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

def add_rows(icon, new_en, new_ru):
    assert len(new_en) == len(new_ru), f"{icon}: EN/RU count mismatch"
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"
    existing_en = set(read_texts(en_path))
    existing_ru = set(read_texts(ru_path))
    add_en = [(t, icon) for t in new_en if t not in existing_en]
    add_ru = [(t, icon) for t in new_ru if t not in existing_ru]
    append_csv(en_path, add_en)
    append_csv(ru_path, add_ru)
    print(f"  {icon}: +{len(add_en)} EN  +{len(add_ru)} RU")
```

**Batch script naming convention:**
```
gen_icons_task_001.py   — first batch of 20 icons
gen_icons_task_002.py   — next batch of 20 icons
...
```

---

### Step 3 — Rebuild merged dataset

After every batch:
```bash
python3 scripts/merge_icon_datasets.py --lang en --allow-missing
python3 scripts/merge_icon_datasets.py --lang ru --allow-missing
```

---

### Step 4 — Audit and verify

```bash
python3 scripts/audit_icon_dataset.py
```

Target metrics after completion:
- All icons ≥ 60 EN rows
- All icons ≥ 60 RU rows
- 0 icons with missing RU data
- 0 cross-icon ambiguous texts (≥3 icons)

---

### Step 5 — Commit after each batch

```bash
git add -A
git commit -m "Add task-style phrases: batch N (icons X–Y)"
```

---

## Quality Checklist (per icon, per phrase)

Before writing any phrase, ask:

- [ ] Would a real Smarter Day user type this as a task title?
- [ ] Is it specific enough to point to this icon and not a neighbor?
- [ ] Does it sound natural in the language (EN or RU)?
- [ ] Is it NOT a visual description of the icon?
- [ ] Is it NOT a developer/designer phrase?
- [ ] Do the boundary phrases describe a DIFFERENT icon?
- [ ] Are EN and RU counts equal?

---

## Example: Correct Batch Script

```python
#!/usr/bin/env python3
"""Batch task-001: Add task-style phrases to 20 lowest-coverage icons."""

import csv
from pathlib import Path

icons_dir = Path(__file__).parent / "icons"

def read_texts(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r["text"].strip() for r in csv.DictReader(f)]

def append_csv(path, rows):
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

def add_rows(icon, new_en, new_ru):
    assert len(new_en) == len(new_ru), f"{icon}: EN/RU mismatch"
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"
    existing_en = set(read_texts(en_path))
    existing_ru = set(read_texts(ru_path))
    add_en = [(t, icon) for t in new_en if t not in existing_en]
    add_ru = [(t, icon) for t in new_ru if t not in existing_ru]
    append_csv(en_path, add_en)
    append_csv(ru_path, add_ru)
    print(f"  {icon}: +{len(add_en)} EN  +{len(add_ru)} RU")

# ── example: scrubber ─────────────────────────────────────────────────────────
add_rows("scrubber",
    new_en=[
        # keywords
        "scrubber",
        "media timeline scrubber",
        "playback position",
        # direct tasks
        "drag the scrubber to the right chapter",
        "seek to 2 minutes in the podcast",
        "jump to the chorus in the track",
        "rewind the video to the beginning",
        "skip ahead using the timeline scrubber",
        # contextual
        "set the playback position for the clip",
        "scrub back to find that quote in the podcast",
        "find the right moment in the video",
        # short
        "seek video",
        "scrub audio",
        "timeline position",
        # conversational
        "need to rewind to where I left off",
        "drag back to that part of the recording",
        # typos
        "scrubber drgged to rewind",
        "timelin positon in player",
        "seek to timestmap",
        "drag the scruber",
        # boundary: progress-bar (not scrubber dot)
        "upload progress 80 percent complete",
        "download bar filling up",
        "task completion percentage shown",
        "loading progress bar for the file",
        "fill level shown as a horizontal bar",
    ],
    new_ru=[
        # keywords
        "ползунок",
        "ползунок временной шкалы",
        "позиция воспроизведения",
        # direct tasks
        "перетащить ползунок к нужной главе",
        "перейти к 2-й минуте в подкасте",
        "перемотать к припеву",
        "перемотать видео к началу",
        "пропустить вперёд по временной шкале",
        # contextual
        "установить позицию воспроизведения для клипа",
        "отмотать назад к нужной цитате в подкасте",
        "найти нужный момент в видео",
        # short
        "перемотать видео",
        "ползунок аудио",
        "позиция на шкале",
        # conversational
        "нужно вернуться к тому месту где остановился",
        "перетащить к этому фрагменту записи",
        # typos
        "ползунок прертащен назад",
        "позиция на временой шкале",
        "перейти к временнйо метке",
        "потащить ползунек",
        # boundary: progress-bar
        "загрузка 80 процентов завершена",
        "полоса загрузки заполняется",
        "процент выполнения задачи показан",
        "полоса прогресса загрузки файла",
        "уровень заполнения показан горизонтальной полосой",
    ],
)

print("\nDone. Run merge and audit next.")
```

---

## Boundary Icon Reference

When writing boundary phrases, always pick icons that are visually or semantically close.
Check `docs/icon-semantic-groups.yml` for known groups.

Common boundary pairs to be aware of:
| Icon | Likely boundary icons |
|------|-----------------------|
| loader | progress-bar, hourglass, spinner |
| scrubber | progress-bar, slider |
| bin-recycle | bin-bottles, trash, wastebasket |
| bin-bottles | bin-recycle, water-bottle |
| capsule | capsules, tablet (pill), prescription |
| capsules | capsule, tablet (pill), syringe |
| chair | chair-office, couch, bench |
| chair-office | chair, couch, desk |
| window (app) | browser, display, monitor |
| tablet (device) | laptop, phone, e-reader |
| users | user (single), group, people |
| dove | bird, crow, pigeon |
| chess-board | game, board, strategy |
| cloud-meatball | food, pasta, rainy |

---

## Session Startup Checklist

When starting a new chat session to work on this plan:

1. Read this file: `docs/plans/icon-dataset-rewrite-plan.md`
2. Run audit to see current state:
   ```bash
   python3 scripts/audit_icon_dataset.py 2>&1 | head -20
   ```
3. Find next batch of icons to expand:
   ```bash
   python3 - <<'EOF'
   import csv
   from pathlib import Path
   stats = [(sum(1 for _ in csv.DictReader(open(d/"train_en.csv"))), d.name)
            for d in Path("icons").iterdir()
            if d.is_dir() and (d/"train_en.csv").exists()]
   stats.sort()
   for r, n in stats[:25]:
       print(f"{n}: {r}")
   EOF
   ```
4. Read existing `train_en.csv` and `train_ru.csv` for those icons before writing anything
5. Write batch script following the template above
6. Run script, merge, audit, commit

---

## Do Not

- Do not machine-translate phrases — write Russian naturally
- Do not copy the visual description style from old gen_icons scripts
- Do not add developer/designer phrases ("I need a X icon for...")
- Do not add broad single words like "food", "travel", "tool" without context
- Do not write boundary phrases that still describe the current icon
- Do not make EN and RU row counts unequal
- Do not run parallel agents (user preference)

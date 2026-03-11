# Icon Dataset Agent Context

## Purpose
Generate a bilingual (EN + RU) training dataset for a Core ML BERT text classifier.
The model maps user task text → FontAwesome icon in the Smarter Day iOS app.
**Primary signal:** user types a task title → model suggests a matching icon.

---

## Current Dataset State (2026-03-11)
- **711 icons** in the main set (`icon_browser/icons-data.js`)
- **711 icons** have training data in `icons/`
- Avg EN train rows per icon: **~37** (target: 60+)
- Icons with < 30 EN rows: **~141**
- Icons with 30–49 EN rows: **~521**
- Candidates for future addition: **~3493** in `icon_browser/candidates-data.js`

**Active plan:** `docs/plans/icon-dataset-rewrite-plan.md`

---

## File Structure

```
core_ml_icons/
├── icons.json                      ← source of truth: all icons + search terms + unicode
├── categories.yml                  ← IRRELEVANT_ICONS filter for the browser
├── AGENT_CONTEXT.md                ← this file
│
├── icons/{icon_name}/              ← training data per icon
│   ├── train_en.csv                — text,label
│   ├── train_ru.csv
│   ├── valid_en.csv
│   ├── test_en.csv
│   ├── valid_ru.csv
│   ├── test_ru.csv
│   └── icon_log.json
│
├── merged_icons_dataset/           ← rebuilt by merge_icon_datasets.py
├── scripts/
│   ├── audit_icon_dataset.py       ← run after every change
│   ├── merge_icon_datasets.py      ← merge: --lang en --allow-missing
│   ├── remove_devspeak.py          ← remove "I need a X icon for..." patterns
│   └── remove_crossicon_ambiguous.py
│
├── docs/
│   ├── icon-dataset-editorial-guide.md
│   ├── icon-semantic-groups.yml    ← groups of semantically close icons
│   ├── icon-semantic-coverage.json ← full coverage: grouped, pair-risk, isolated
│   └── plans/
│       └── icon-dataset-rewrite-plan.md   ← CURRENT WORK PLAN
│
└── icon_browser/
    ├── index.html
    ├── icons-data.js               ← window.ICON_DATA (711 icons)
    └── candidates-data.js          ← window.IRRELEVANT_ICONS + window.CANDIDATE_DATA
```

---

## Editorial Rules (Non-Negotiable)

1. **No automatic phrase generation.** Every phrase is written or reviewed by a human.
2. **No raw machine translation.** Translation tools can be used as a rough draft only.
3. **EN and RU must stay in sync.** Every new `train_en` row needs a `train_ru` row with the same intent. Same for valid/test.
4. **Task-first phrasing.** The default question is: *"What would a user type as a task title to expect this icon?"*
   - ✅ `buy bell peppers` / `купить болгарский перец`
   - ❌ `bright red pepper with green stem` (visual description)
   - ❌ `I need a pepper icon for my recipe app` (developer-speak)
5. **No overly broad terms** without context: `food`, `travel`, `tool`, `holiday`.
6. **Boundary phrases** (describes a DIFFERENT neighbouring icon) must NOT go into `train_en.csv` or `train_ru.csv`. They stay in `icon_log.json` only.

---

## New Phrase Template (Task-First)

Use this for all new data. Target: **60 rows per icon** (EN) + **60 rows** (RU).

### EN categories

| # | Category | Count | Example (pepper) |
|---|----------|-------|-----------------|
| 1 | Keyword / search term | 3–5 | `bell pepper`, `capsicum` |
| 2 | Direct task — action verb | 8–10 | `buy bell peppers`, `slice peppers for stir fry` |
| 3 | Contextual task — with time or purpose | 6–8 | `peppers for Sunday dinner`, `don't forget peppers for taco night` |
| 4 | Short / power-user | 4–5 | `need peppers`, `peppers - grocery run` |
| 5 | Conversational | 4–5 | `we're out of peppers — need to buy some` |
| 6 | Realistic typos | 4 | `pepepr sliced`, `bel pepper from store` |
| 7 | Boundary (in `icon_log.json` only — NOT in train CSV) | 5–6 | describes avocado/chili/tomato |

### RU follows the same structure
Write naturally in Russian — not a literal translation.
```
болгарский перец          ← keyword
купить болгарский перец   ← direct task
перцы для воскресного ужина  ← contextual
нужны перцы              ← short
перцы закончились — надо купить  ← conversational
перец нарблен для стир-фрая  ← typo
```

---

## Current Workflow: Expand Existing Icons

### Step 0 — Check current state
```bash
python3 scripts/audit_icon_dataset.py 2>&1 | head -20

# Find lowest-coverage icons:
python3 - <<'EOF'
import csv
from pathlib import Path
stats = [(sum(1 for _ in csv.DictReader(open(d/"train_en.csv"))), d.name)
         for d in Path("icons").iterdir()
         if d.is_dir() and (d/"train_en.csv").exists()]
for r, n in sorted(stats)[:25]:
    print(f"{n}: {r}")
EOF
```

### Step 1 — Read existing data before writing anything
```bash
cat icons/{icon}/train_en.csv
cat icons/{icon}/train_ru.csv
```
Check for: boundary rows that snuck into train, bad machine translations,
visual descriptions, developer-speak.

### Step 2 — Write batch script

Name: `gen_icons_task_NNN.py` (increment NNN each batch).

**Standard helper:**
```python
import csv
from pathlib import Path

icons_dir = Path("icons")

def read_texts(path):
    if not path.exists(): return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r["text"].strip() for r in csv.DictReader(f)]

def remove_rows(path, bad: set) -> int:
    if not path.exists(): return 0
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    kept = [r for r in rows if r["text"].strip() not in bad]
    removed = len(rows) - len(kept)
    if removed:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["text", "label"])
            w.writeheader()
            w.writerows(kept)
    return removed

def append_csv(path, rows):
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

def expand(icon, new_en, new_ru, fix_en=None, fix_ru=None):
    """Add new rows; optionally remove known-bad rows first."""
    assert len(new_en) == len(new_ru), f"{icon}: EN/RU count mismatch"
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"
    rem_en = remove_rows(en_path, set(fix_en or []))
    rem_ru = remove_rows(ru_path, set(fix_ru or []))
    existing_en = set(read_texts(en_path))
    existing_ru = set(read_texts(ru_path))
    add_en = [(t, icon) for t in new_en if t not in existing_en]
    add_ru = [(t, icon) for t in new_ru if t not in existing_ru]
    append_csv(en_path, add_en)
    append_csv(ru_path, add_ru)
    fix_note = f" (fixed EN:{rem_en} RU:{rem_ru})" if (rem_en or rem_ru) else ""
    print(f"  {icon}: +{len(add_en)} EN  +{len(add_ru)} RU{fix_note}")
```

### Step 3 — Run, merge, audit, commit
```bash
python3 gen_icons_task_NNN.py
python3 scripts/merge_icon_datasets.py --lang en --allow-missing
python3 scripts/merge_icon_datasets.py --lang ru --allow-missing
python3 scripts/audit_icon_dataset.py | head -20
git add -A && git commit -m "Add task-style phrases: batch NNN (icons X–Y)"
```

---

## Adding New Icons (if needed)

### Get search terms from icons.json
```python
import json
with open("icons.json") as f:
    data = json.load(f)
targets = ["anchor", "bell"]
for key, val in data.items():
    name = val.get("label","").lower().replace(" ","-")
    if name in targets:
        print(name, val.get("search",{}).get("terms",[]))
```

### Update icon_browser after adding
```python
# See full script in git history (gen_icons_* scripts, Step 5)
# Key: update icons-data.js, then regenerate candidates-data.js
# Candidates sort: key=lambda x: (len(x['name'].split('-')), x['name'])
```

---

## Quality Checklist (per phrase)

- [ ] Sounds like a real task title a user would type in Smarter Day?
- [ ] Specific enough to point to this icon, not a neighbour?
- [ ] Natural in the language (EN or RU)?
- [ ] NOT a visual description of the icon?
- [ ] NOT a developer/designer phrase?
- [ ] Boundary phrases are in `icon_log.json` only, NOT in train CSV?
- [ ] EN and RU row counts are equal?

---

## Common Mistakes

| Wrong | Correct |
|-------|---------|
| `bnd_en` rows in `train_en.csv` | boundary stays in `icon_log.json` only |
| `"bright red pepper with green stem"` in train | use task-style: `"buy bell peppers"` |
| `"I need a pepper icon for my app"` | not a user task — remove |
| Raw machine translation in RU | write naturally, use translation as draft only |
| EN and RU row counts unequal | always assert equal counts in script |
| `icons_data/` directory | save to `icons/` |
| search terms from `icons.claude.json` | always use `icons.json` |

# How to Build the Per-Icon Phrase Plan

## Goal
Create `docs/plans/per-icon-phrase-plan.md` — a detailed, per-icon reference that tells
any agent exactly what task-style phrases to write for each of the 695 icons that still
need more training data.

---

## Context
- App: Smarter Day iOS task manager
- Model: Core ML BERT text classifier, 711 classes
- Input: user types a task title → model suggests an icon
- Training data lives in: `icons/{icon_name}/train_en.csv` and `train_ru.csv`
- Target: 60 EN rows + 60 RU rows per icon (currently avg ~35)
- Plan to reference: `docs/plans/icon-dataset-rewrite-plan.md`

---

## What the Per-Icon Plan File Should Contain

One entry per icon, in this compact format:

```
### icon-name (current: N rows → add ~X)
**Domain:** cooking / finance / sport / tech / etc.
**Tasks EN:** short task 1, medium task phrase 2, task phrase 3, task phrase 4, task 5
**Tasks RU:** задача 1, задача 2, задача 3, задача 4
**Boundary:** similar-icon-1, similar-icon-2
```

Rules for task phrases:
- Must sound like a task title a real user types in a to-do app
- Mix: 1-2 word keywords + 4-8 word task phrases + occasional longer ones
- ✅ "buy bell peppers", "slice peppers for stir fry", "peppers for taco night"
- ❌ "bright red pepper icon", "I need a pepper symbol for my app"

---

## Step-by-Step Execution

### Step 1 — Run this to get all icon data
```bash
python3 - <<'EOF'
import csv, json
from pathlib import Path

icons_dir = Path("icons")
with open("icons.json") as f:
    icons_data = json.load(f)

term_map = {}
for key, val in icons_data.items():
    name = val.get("label","").lower().replace(" ","-")
    terms = val.get("search",{}).get("terms",[])
    term_map[name] = terms

stats = []
for d in sorted(icons_dir.iterdir()):
    if not d.is_dir(): continue
    f = d / "train_en.csv"
    if not f.exists(): continue
    with f.open() as fp:
        rows = sum(1 for _ in csv.DictReader(fp))
    if rows < 60:
        stats.append((rows, d.name, term_map.get(d.name, [])))

stats.sort()
for r, n, t in stats:
    print(f"{n} ({r}): {', '.join(t[:6])}")
EOF
```

### Step 2 — Write the plan file in batches of 30 icons

Process 30 icons at a time. For each icon:
1. Look at its name and search terms
2. Think: what task would a user create that needs this icon?
3. Write 5 EN task examples + 4 RU task examples
4. Identify 1-2 boundary icons (semantically closest neighbours)

Write to: `docs/plans/per-icon-phrase-plan.md`

Start with a header section, then append each batch of 30.

### Step 3 — After all batches are written

Commit the file:
```bash
git add docs/plans/per-icon-phrase-plan.md
git commit -m "Add per-icon phrase plan for 695 icons"
```

---

## Batches to Process (695 icons total)

| Batch | Coverage | Icons | Priority |
|-------|----------|-------|----------|
| 1 | < 30 rows | 216 | Highest |
| 2 | 30–39 rows | 286 | High |
| 3 | 40–49 rows | 164 | Medium |
| 4 | 50–59 rows | 29 | Low |

Process Batch 1 first (most urgent), then 2, 3, 4.

---

## Domain Reference (use when classifying icons)

| Domain | Example icons |
|--------|--------------|
| Food & cooking | pepper, pot-food, pan-frying, knife-kitchen, oven |
| Sport & fitness | pickleball, basketball, dumbbell, kettlebell, racquet |
| Finance | piggy-bank, wallet, coins, dollar-sign, sack-dollar |
| Health & medical | tablets, pills, thermometer, syringe, heart-pulse |
| Tech & devices | tablet, tv, laptop, keyboard, computer, router |
| Transport & logistics | tractor, trailer, ramp-loading, truck, van |
| Entertainment | pinball, podcast, joystick, gamepad, guitar |
| Home & household | shower, sink, washing-machine, vacuum, refrigerator |
| Clothing & fashion | shoe, bra, shirt, jeans, scarf, socks |
| Nature & animals | mosquito, deer, duck, frog, squirrel |
| Holidays & seasonal | wreath, stocking, star-christmas, snow-blowing, ornament |
| Office & productivity | stapler, trash, signature, pen, paperclip |
| Travel | trailer, passport, ticket-airline, suitcase, caravan |
| Fantasy & gaming | pinball, mace, sickle, wand, scroll, helmet-battle |

---

## Example Entry (reference quality)

```
### pot-food (23 → add 37)
**Domain:** cooking / home
**Tasks EN:** make soup for dinner, cook a big pot of stew, simmer broth on the stove,
  prepare soup for the week, pot of chili for the game, cook lentil soup, reheat the soup
**Tasks RU:** сварить суп на ужин, приготовить рагу, поставить бульон на плиту,
  суп на неделю, разогреть суп
**Boundary:** bowl-hot (bowl of soup), kitchen-set (full kitchen), cauldron (big pot halloween)

### pickleball (23 → add 37)
**Domain:** sport / recreation
**Tasks EN:** play pickleball this weekend, book pickleball court, buy a pickleball paddle,
  pickleball practice tonight, sign up for pickleball tournament, pickleball with friends
**Tasks RU:** сыграть в пиклбол на выходных, забронировать корт для пиклбола,
  купить ракетку для пиклбола, тренировка по пиклболу
**Boundary:** tennis-ball (tennis), racquet (badminton/squash), shuttlecock (badminton)
```

---

## Notes
- Do NOT add developer-speak: "I need a X icon for my app"
- Do NOT add visual descriptions: "orange ball with holes in it"
- Boundary icons go in `icon_log.json` only, NOT in train CSV
- EN and RU counts must stay equal when writing actual data later

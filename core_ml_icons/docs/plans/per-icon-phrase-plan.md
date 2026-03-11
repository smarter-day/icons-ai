# Per-Icon Phrase Plan

**Purpose:** Full pipeline to produce a training-ready dataset across all 6 languages.

**Languages (Tier 1):** English, German, Japanese, French, Spanish, Russian.
Each icon needs phrases in all 6 languages. Files: `train_en.csv`, `train_de.csv`, `train_ja.csv`,
`train_fr.csv`, `train_es.csv`, `train_ru.csv` inside `icons/{name}/`.

**Target per icon per language:** 60 train rows + 8 valid rows + 8 test rows.

---

## Pipeline overview

```
Step 0 — Pre-flight: verify scripts, permissions, baseline state
Step 1 — Audit existing EN/RU data; top up EN/RU valid/test to 8 rows
Step 2 — Quality review of existing EN/RU train phrases (agent)
Step 3 — Generate train phrases (agent, all 6 languages, all 711 icons)
Step 4 — Generate valid + test phrases (agent, all 6 languages, all 711 icons)
Step 5 — Rebuild merged dataset
Step 6 — Final audit before training
```

---

## Step 0 — Pre-flight

Complete this step fully before starting any generation work. Goal: no interruptions later.

### 0.1 — Verify write access

```bash
touch icons/anchor/test_write && rm icons/anchor/test_write && echo "OK"
```

If this fails, fix directory permissions before proceeding.

### 0.2 — Verify scripts exist and support new languages

All scripts used in this pipeline:

| Script | Used in |
|--------|---------|
| `scripts/audit_icon_dataset.py` | Step 1, Step 6 |
| `scripts/merge_icon_datasets.py` | Step 5 |

Run both with a new language to confirm they work:

```bash
python3 scripts/merge_icon_datasets.py --lang de --allow-missing --dry-run
python3 scripts/audit_icon_dataset.py --lang de
```

If either script fails or ignores new language files, update it to accept any `--lang` value
before proceeding. The audit script must be able to report coverage per language,
otherwise Step 6 final checks will be unreliable.

### 0.3 — Verify icons.json is readable

```bash
python3 -c "import json; d=json.load(open('icons.json')); print(f'OK: {len(d)} icons')"
```

### 0.4 — Check current dataset state

Run the progress tracking script (also in Step 3) to understand the starting point:

```python
import csv
from pathlib import Path

langs = ["en", "de", "ja", "fr", "es", "ru"]
targets = {lang: 60 for lang in langs}

incomplete = []
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    for lang in langs:
        f = d / f"train_{lang}.csv"
        rows = sum(1 for _ in csv.DictReader(open(f))) if f.exists() else 0
        if rows < targets[lang]:
            incomplete.append((d.name, lang, rows, targets[lang] - rows))

print(f"Total icons: {sum(1 for d in Path('icons').iterdir() if d.is_dir())}")
print(f"Incomplete train files: {len(incomplete)} icon/language pairs")
print(f"Total phrases to generate: {sum(n for _,_,_,n in incomplete)}")
```

---

## Step 1 — Audit existing EN/RU data

Run audit to detect problems in current EN and RU data before adding new phrases.
Only EN and RU have existing data; DE/JA/FR/ES start from zero.

```bash
python3 scripts/audit_icon_dataset.py
```

Review the output for:
- Icons with devspeak phrases (visual descriptions, "I need a X icon for my app")
- Boundary phrases accidentally placed in train instead of icon_log.json
- Ambiguous texts appearing under 3+ different icon labels

Fix only confirmed issues. Do not run cleanup scripts blindly — review each flagged
phrase before removing. When in doubt, keep the phrase.

Also check current EN/RU valid and test coverage — they may be below the 8-row target:

```python
import csv
from pathlib import Path

langs = ["en", "ru"]
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    for lang in langs:
        for split in ["valid", "test"]:
            f = d / f"{split}_{lang}.csv"
            rows = sum(1 for _ in csv.DictReader(open(f))) if f.exists() else 0
            if rows < 8:
                print(f"{d.name}/{lang} {split}: {rows} rows (need {8 - rows} more)")
```

Top up any EN/RU valid/test files that are below 8 rows before generating new language data.

---

## Step 2 — Quality review of existing EN/RU train phrases

Only EN and RU have existing train data. Before adding new phrases, the agent reviews
every existing phrase in `train_en.csv` and `train_ru.csv` for each icon and removes
anything that violates current quality rules.

This step is done by the agent — not by a script — because quality judgement is contextual.

### What to remove

Remove a phrase if it matches any of these:

| Problem | Example |
|---------|---------|
| Visual description | "bright red pepper with green stem" |
| Developer-speak | "I need a pepper icon for my recipe app" |
| Generic single word that fits 5+ icons | "health", "food", "sport" |
| Nonsensical or clearly wrong for this icon | "buy a car" in `pot-food` |
| Duplicate of another phrase in the same file | exact or near-exact match |

### What to keep

When in doubt — keep the phrase. Only remove clear violations.
Do NOT remove phrases just because they're short, simple, or imperfect.
A phrase like "soup" is fine — it's a valid keyword.

### After review

After removing bad phrases, recalculate how many new phrases are needed:
`needed = 60 - remaining_rows`

This updated count feeds directly into Step 3 — the agent uses it to know
how many phrases to generate for each icon.

If removing bad phrases brings an icon below 60, that's expected — Step 3 fills the gap.
If an icon still has ≥ 60 good phrases after review, skip it in Step 3 for EN/RU.

---

## Step 3 — Generate train phrases

### CSV format

Every train/valid/test file must have exactly two columns: `text` and `label`.
The `label` value is always the icon name (e.g. `pot-food`) — must exactly match
the directory name. A typo like `pot_food` creates a silent new class in the model.
Encoding: UTF-8 (required for Japanese, Russian, German umlauts).

```csv
text,label
make soup for dinner,pot-food
夕食にスープを作る,pot-food
Suppe zum Abendessen kochen,pot-food
```

**Create vs append:**
- EN/RU files already exist → append new rows
- DE/JA/FR/ES files do not exist yet → create new file with header `text,label`

After writing, verify labels are correct:

```python
import pandas as pd
from pathlib import Path

langs = ["en", "de", "ja", "fr", "es", "ru"]
for d in Path("icons").iterdir():
    if not d.is_dir(): continue
    for lang in langs:
        f = d / f"train_{lang}.csv"
        if not f.exists(): continue
        df = pd.read_csv(f)
        bad = df[df["label"] != d.name]
        if not bad.empty:
            print(f"{d.name}/{lang}: {len(bad)} rows with wrong label: {bad['label'].unique()}")
```

### How generation works

Phrases are written by an LLM agent — not generated by scripts.
For each icon and language the agent:
1. Checks how many rows already exist in `icons/{name}/train_{lang}.csv`
2. Calculates how many to add: `needed = 60 - existing_rows`
3. If `needed ≤ 0` — skip this icon/language, it's already complete
4. Reads the icon name and search terms from `icons.json`
5. Thinks about what tasks a real user would create with this icon
6. Writes exactly `needed` phrases into the file
   - EN/RU: append to existing file
   - DE/JA/FR/ES: create new file with header `text,label` if it doesn't exist yet

Scripts are only used for auditing, merging, and checking — not for writing phrases.

### Phrase rules

- Phrases must sound like real to-do app task titles a user types in Smarter Day
- Mix ~30% short keywords (1–2 words) with ~70% task phrases (4–8 words)
- Write naturally in each language — do NOT translate literally from English
- ❌ No visual descriptions ("orange ball with holes"), no developer-speak ("I need a X icon")
- Boundary icons: note them to avoid semantic overlap, but do NOT add them to train CSV
- Process all 6 languages for one icon at a time — keeps context consistent

### Phrase diversity rule

Across 60 train phrases for one icon, use at least 3 different structural patterns:
- **Action + object:** "buy bell peppers", "купить болгарский перец"
- **Full task sentence:** "pick up groceries after work", "зайти в магазин после работы"
- **Short keyword:** "grocery run", "продукты"
- **Context phrase:** "weekly shopping list", "список покупок на неделю"

Don't write 60 variations of the same structure — vary the form, not just the words.

### Typos

Include ~5 realistic typo phrases per icon per language in train data.
These count toward the 60 total — write 55 normal phrases + 5 typo phrases = 60 rows.
Users mistype task titles — the model must handle this.

Three types of realistic typos only:
- **Transposition** (adjacent letters swapped): `piclebkall`, `shppoing`
- **Missing letter**: `shoping`, `trainging`
- **Adjacent key**: `vaccuum` (c→cc), `brocolli`

```
# ✅ GOOD — realistic keyboard errors
shoping list        ← missing p
vaccum the floor    ← adjacent key
piclebkall court    ← transposition

# ❌ BAD — not realistic
xzqwerty icon
sh0pping l1st
```

Typos go in `train_{lang}.csv` only — not in valid or test.

### Quality checklist

Before finalising phrases for an icon:
- [ ] Do phrases sound like real task titles a human would type?
- [ ] Are there at least 3 different structural patterns?
- [ ] Are ~5 typo phrases included per language?
- [ ] Do phrases avoid visual descriptions and developer-speak?
- [ ] Would any phrase fit a boundary icon better? (if yes, rewrite it)

### Language-specific notes

**German (DE):** Use compound nouns naturally (e.g. "Einkaufsliste", "Arzttermin").
German users phrase tasks concisely.

**Japanese (JA):** Write without spaces between words — natural Japanese has no word spacing.
Phrases should be short and direct (e.g. 夕食を作る, 病院の予約). Avoid overly formal keigo.
Use katakana for foreign words (e.g. ピックルボール, スーパー).

**French (FR):** Use infinitive form for task titles (e.g. "acheter du pain", "réserver le restaurant").

**Spanish (ES):** Use infinitive form similarly (e.g. "comprar verduras", "ir al gimnasio").
Both Spain and Latin American phrasings are acceptable.

**Russian (RU):** Use short imperative or noun phrases (e.g. "купить продукты", "записаться к врачу").

### Culturally specific and ambiguous icons

Some icons are specific to one culture or mean different things across languages.
Always think from the perspective of a native speaker in that language.

**Culturally specific** — shift to nearest local equivalent when concept is unfamiliar:
- badge-sheriff → DE/FR/ES/RU: police officer, security badge, Halloween costume prop
- football (American) → DE/FR/ES/JA: always write "American football" explicitly,
  or focus on watching/buying rather than playing
- police-box → JA: use ドクター・フー (Doctor Who) or sci-fi prop context
- stroopwafel → JA/RU: treat as an exotic snack, focus on buying or tasting
- hockey-mask → DE/FR/ES: Halloween costume context, or ice hockey goalie

**Ambiguous across languages** — icons whose English name maps to different concepts:
- football → EN means American football; DE/FR/ES/RU means soccer. Use separate
  phrases per language reflecting local meaning. Do NOT mix.
- pants → EN means trousers; BE English means underwear. Use "trousers" framing for non-US.
- smoking → could be BBQ smoking (food) or cigarette smoking. Check icon domain before writing.

### Icons not in batches (≥60 EN rows after Step 2 review)

These icons have enough EN phrases but need all other languages from scratch.
Run this AFTER Step 2 (quality review) to get the accurate list — some icons
may have dropped below 60 after removing bad phrases and will no longer qualify:
Generate 60 train phrases for DE/JA/FR/ES for each icon in this list.

```bash
python3 - <<'EOF'
import csv
from pathlib import Path
for d in sorted(Path("icons").iterdir()):
    f = d / "train_en.csv"
    if f.exists():
        rows = sum(1 for _ in csv.DictReader(open(f)))
        if rows >= 60:
            print(d.name, rows)
EOF
```

### Format per icon

```
### icon-name (EN rows → add N; DE/JA/FR/ES: 0 → 60)
Domain: <category>
Tasks EN: phrase 1, phrase 2, phrase 3, phrase 4, phrase 5
Tasks DE: Aufgabe 1, Aufgabe 2, Aufgabe 3, Aufgabe 4
Tasks JA: タスク1, タスク2, タスク3, タスク4
Tasks FR: tâche 1, tâche 2, tâche 3, tâche 4
Tasks ES: tarea 1, tarea 2, tarea 3, tarea 4
Tasks RU: задача 1, задача 2, задача 3, задача 4
Boundary: similar-icon-1, similar-icon-2
```

### Examples across different domains

```
### pot-food (23 → add 37; DE/JA/FR/ES: 0 → 60)
Domain: cooking / home
Tasks EN: make soup for dinner, cook a big pot of stew, simmer broth on the stove,
  prepare soup for the week, pot of chili for the game
Tasks DE: Suppe zum Abendessen kochen, großen Eintopf zubereiten, Brühe auf dem Herd köcheln,
  Suppe für die Woche vorbereiten
Tasks JA: 夕食にスープを作る, シチューを大鍋で煮込む, 一週間分のスープを準備する, だし汁を火にかける
Tasks FR: préparer une soupe pour le dîner, cuire un ragoût, mijoter un bouillon, soupe pour la semaine
Tasks ES: hacer sopa para cenar, cocinar un guiso, preparar caldo, sopa para toda la semana
Tasks RU: сварить суп на ужин, приготовить рагу, поставить бульон на плиту, суп на неделю
Boundary: bowl-food (bowl of soup), kitchen-set (full kitchen)

### piggy-bank (23 → add 37; DE/JA/FR/ES: 0 → 60)
Domain: finance / savings
Tasks EN: add money to savings, set up piggy bank for kids, save for vacation fund,
  transfer to savings account, track monthly savings goal
Tasks DE: Geld sparen, Sparschwein für Kinder einrichten, für den Urlaub sparen,
  monatliches Sparziel verfolgen
Tasks JA: 貯金する, 子供の貯金箱を用意する, 旅行のために貯金, 毎月の貯蓄目標を確認する
Tasks FR: mettre de l'argent de côté, tirelire pour les enfants, économiser pour les vacances,
  suivre l'objectif d'épargne mensuel
Tasks ES: ahorrar dinero, alcancía para los niños, ahorrar para las vacaciones,
  revisar el objetivo de ahorro mensual
Tasks RU: пополнить копилку, откладывать деньги на отпуск, сберегательный счёт, цель по накоплениям
Boundary: wallet (everyday spending), dollar-sign (money)

### pickleball (23 → add 37; DE/JA/FR/ES: 0 → 60)
Domain: sport / recreation
Tasks EN: play pickleball this weekend, book pickleball court, buy a pickleball paddle,
  pickleball practice tonight, sign up for pickleball tournament
Tasks DE: Pickleball am Wochenende spielen, Pickleballplatz buchen, Pickleball-Schläger kaufen,
  für das Pickleball-Turnier anmelden
Tasks JA: 週末にピックルボールをする, ピックルボールコートを予約する, パドルを買う, 大会に申し込む
Tasks FR: jouer au pickleball ce week-end, réserver un terrain de pickleball, acheter une raquette,
  s'inscrire au tournoi de pickleball
Tasks ES: jugar pickleball este fin de semana, reservar cancha de pickleball, comprar paleta de pickleball,
  inscribirse en el torneo de pickleball
Tasks RU: сыграть в пиклбол на выходных, забронировать корт для пиклбола,
  купить ракетку для пиклбола, тренировка по пиклболу
Boundary: tennis-ball (tennis), racquet (badminton/squash)
```

### Progress tracking

With 711 icons × 6 languages this work spans multiple sessions. Before starting a session,
run this to see what's already done and what remains:

```python
import csv
from pathlib import Path

langs = ["en", "de", "ja", "fr", "es", "ru"]
targets = {"en": 60, "ru": 60, "de": 60, "ja": 60, "fr": 60, "es": 60}

incomplete = []
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    for lang in langs:
        f = d / f"train_{lang}.csv"
        rows = sum(1 for _ in csv.DictReader(open(f))) if f.exists() else 0
        if rows < targets[lang]:
            incomplete.append((d.name, lang, rows, targets[lang] - rows))

print(f"Incomplete: {len(incomplete)} icon/language pairs")
for name, lang, have, need in incomplete[:20]:
    print(f"  {name}/{lang}: {have} rows, need {need} more")
```

Resume from where you left off — process icons in the order they appear in the batches below.

### Progress output

After completing each icon, print a status line to console — do NOT pause or ask for confirmation:

```python
# After writing phrases for one icon:
pct = done / total * 100
print(f"[{pct:.1f}%] {icon_name}: EN +{added_en}, RU +{added_ru}, DE +{added_de}, JA +{added_ja}, FR +{added_fr}, ES +{added_es}")
```

Example output:
```
[0.1%] pickleball: EN +37, RU +37, DE +60, JA +60, FR +60, ES +60
[0.3%] piggy-bank: EN +37, RU +37, DE +60, JA +60, FR +60, ES +60
[0.4%] pinball: EN skipped, RU +35, DE +60, JA +60, FR +60, ES +60
```

Print a summary every 30 icons:
```python
pct = done / total * 100
print(f"--- {pct:.0f}% done ({done}/{total} icons) | {total_added} phrases written so far ---")
```

### Batch 1 — < 30 rows (216 icons, highest priority)

**Note:** Row counts below are pre-quality-review estimates based on current EN data.
After Step 2 removes bad phrases, actual counts will be lower — use the progress tracking
script at the top of Step 3 to get the real "needed" number for each icon.

Add EN/RU phrases to reach 60 (exact count from progress script). Add 60 DE/JA/FR/ES phrases per icon (from 0).
Append to `icons/{name}/train_{lang}.csv`.

**23 rows → add 37** (12 icons):
pickleball, piggy-bank, pinball, podcast, pot-food, ramp-loading, tablets, tractor,
traffic-cone, trailer, trash, weight-scale

**24 rows → add 36** (12 icons):
badge-sheriff, book-quran, hands, pan-frying, pills, racquet, screencast, shuttlecock,
signature, sportsball, thermometer, tv

**25 rows → add 35** (23 icons):
bra, broccoli, candy, kettlebell, mosquito, oil-well, peanut, plate-wheat, share-all,
share-nodes, shoe, shower, sink, spinner, stapler, stopwatch, street-view, tire,
toggle-off, train-subway, transporter, truck, watch

**26 rows → add 34** (40 icons):
bag-shopping, bandage, bin-recycle, chair, chess-board, cloud-meatball, dove, eraser,
handshake, heart-pulse, hockey-mask, hospital, laptop, lobster, memory, outlet, paragraph,
passport, paw, pen-paintbrush, potato, rug, rupiah-sign, sandwich, satellite, seat, sensor,
snow-blowing, spoon, star-christmas, steering-wheel, timeline, toggle-on, train-track,
trash-can, video, walker, wallet, warehouse, warehouse-full

**27 rows → add 33** (42 icons):
bolt-lightning, bowl-food, bucket, car-battery, clothes-hanger, command, crop, deer,
diagram-project, diagram-venn, dollar-sign, egg, falafel, flashlight, game-board, glass,
hand-heart, headset, hearts, hotel, key, kitchen-set, motorcycle, mug, music-note, peach,
pen-ruler, person-seat, plate-utensils, rv, scanner-image, sd-card, sickle, sim-card,
slider, spa, stamp, trombone, van, washing-machine, watch-apple, wreath

**28 rows → add 32** (42 icons):
banana, basket-shopping, book-bible, briefcase-medical, butter, cake-slice, chf-sign,
cloud-music, copyright, court-sport, drone-front, dumbbell, fan, file, flatbread-stuffed,
football, glasses, hat-chef, horse-saddle, hryvnia-sign, ice-skate, industry, keyboard,
marker, paperclip, police-box, pump, sack, shield-dog, ship, spray-can, stretcher,
stroopwafel, swatchbook, tag, tennis-ball, tire-rugged, truck-ramp, turntable, umbrella,
vacuum, vacuum-robot

**29 rows → add 31** (45 icons):
bell-school, box-open, boxes-packing, brush, bullseye, bullseye-pointer, carrot, crosshairs,
curling-stone, dog-leashed, drone, duck, fax, flatbread, frog, gamepad, globe-pointer,
guitar, guitar-electric, lips, loveseat, object-group, pan-food, pants, paper-plane, person,
print, qrcode, refrigerator, ruble-sign, sailboat, server, shapes, shelves, shield-cat,
shrimp, shuttle-space, smoking, strawberry, teddy-bear, user-police, volleyball, volume,
wind, x-ray

### Batch 2 — 30–39 rows (286 icons, high priority)

Add EN/RU phrases to reach 60 (exact count from progress script after Step 2). Add 60 DE/JA/FR/ES phrases per icon.
Same rules as above. Use examples as style reference.

Run this script after Step 2 to get the accurate list (some icons may have shifted batches after quality review):

```bash
python3 - <<'EOF'
import csv
from pathlib import Path
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    f = d / "train_en.csv"
    if not f.exists(): continue
    rows = sum(1 for _ in csv.DictReader(open(f)))
    if 30 <= rows < 40:
        print(d.name, rows)
EOF
```

### Batch 3 — 40–49 rows (164 icons, medium priority)

Add EN/RU phrases to reach 60 (exact count from progress script after Step 2). Add 60 DE/JA/FR/ES phrases per icon.
Focus on variety: different contexts, synonyms, alternative phrasings.

Run after Step 2:
```bash
python3 - <<'EOF'
import csv
from pathlib import Path
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    f = d / "train_en.csv"
    if not f.exists(): continue
    rows = sum(1 for _ in csv.DictReader(open(f)))
    if 40 <= rows < 50:
        print(d.name, rows)
EOF
```

### Batch 4 — 50–59 rows (29 icons, low priority)

Add EN/RU phrases to reach 60 (exact count from progress script after Step 2). Add 60 DE/JA/FR/ES phrases per icon.
Only add EN/RU phrases where variety is genuinely missing.

Run after Step 2:
```bash
python3 - <<'EOF'
import csv
from pathlib import Path
for d in sorted(Path("icons").iterdir()):
    if not d.is_dir(): continue
    f = d / "train_en.csv"
    if not f.exists(): continue
    rows = sum(1 for _ in csv.DictReader(open(f)))
    if 50 <= rows < 60:
        print(d.name, rows)
EOF
```

---

## Step 4 — Generate valid + test phrases

For every icon in all 6 languages, ensure each has 8 valid rows and 8 test rows.
- EN/RU: may already have some rows from Step 1 top-up — only add what's missing to reach 8
- DE/JA/FR/ES: start from zero, create file with header and write 8 rows

Do NOT overwrite or regenerate files that already have ≥ 8 rows.
Phrases must be distinct from train and from each other — write from scratch
using different contexts, not paraphrases of train phrases. No typos in valid/test.

Write to:
- `icons/{name}/valid_{lang}.csv` and `icons/{name}/test_{lang}.csv` for all 6 languages.

Check for overlap (train↔test, train↔valid, valid↔test) after generation:

```python
import pandas as pd
from pathlib import Path

langs = ["en", "de", "ja", "fr", "es", "ru"]
for d in Path("icons").iterdir():
    if not d.is_dir(): continue
    for lang in langs:
        files = {
            split: d / f"{split}_{lang}.csv"
            for split in ["train", "valid", "test"]
        }
        sets = {
            split: set(pd.read_csv(f)["text"].str.lower())
            for split, f in files.items() if f.exists()
        }
        for a, b in [("train", "valid"), ("train", "test"), ("valid", "test")]:
            if a in sets and b in sets:
                overlap = sets[a] & sets[b]
                if overlap:
                    print(f"{d.name}/{lang} {a}↔{b}: {len(overlap)} overlapping phrases")
```

Also check for within-file duplicates in train:

```python
import pandas as pd
from pathlib import Path

langs = ["en", "de", "ja", "fr", "es", "ru"]
for d in Path("icons").iterdir():
    if not d.is_dir(): continue
    for lang in langs:
        f = d / f"train_{lang}.csv"
        if not f.exists(): continue
        df = pd.read_csv(f)
        dupes = df[df.duplicated("text", keep=False)]
        if not dupes.empty:
            print(f"{d.name}/{lang}: {len(dupes)} duplicate phrases")
```

---

## Step 5 — Rebuild merged dataset

Run after all train/valid/test files are written:

```bash
for lang in en de ja fr es ru; do
  python3 scripts/merge_icon_datasets.py --lang $lang --allow-missing
done
```

Then combine all languages into single train, valid, and test CSVs:

```python
import pandas as pd

langs = ["en", "de", "ja", "fr", "es", "ru"]

for split in ["train", "valid", "test"]:
    combined = pd.concat([
        pd.read_csv(f"merged_icons_dataset/{split}_{lang}.csv") for lang in langs
    ])
    out = f"{split}_combined.csv"
    combined.to_csv(out, index=False)
    print(f"{out}: {len(combined)} rows, {combined['label'].nunique()} icons")
```

---

## Step 6 — Final audit before training

```bash
python3 scripts/audit_icon_dataset.py
```

Verify:
- All 711 icons have ≥ 60 train rows in each of the 6 languages
- All 711 icons have ≥ 8 valid rows and ≥ 8 test rows in each language
- No train/valid/test phrase overlap (run overlap check from Step 4)
- No within-file duplicates in train files (run duplicate check from Step 4)
- No icon is missing from any language file
- `train_combined.csv`, `valid_combined.csv`, `test_combined.csv` are all up to date

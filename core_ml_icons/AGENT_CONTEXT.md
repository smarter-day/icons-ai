# Icon Dataset Agent Context

## Задача
Генерация датасета для Core ML BERT-эмбеддинг модели — поиск иконок по естественному тексту в приложении Smarter Day iOS. Пользователь вводит название задачи/события → модель предлагает иконку.

## Источник данных об иконках
**`icons.json`** — полная база FontAwesome (~3800+ иконок), формат словаря:
```json
{
  "key": {
    "label": "Anchor",
    "unicode": "f13d",
    "styles": ["solid", "regular"],
    "search": { "terms": ["anchor", "boat", "dock", ...] }
  }
}
```
> Всегда брать `search.terms` из `icons.json` — это официальные поисковые термины иконки.
> Некоторые термины — технические артефакты (Unicode-имена, "uer", дубли) — их пропускать.

## Текущее состояние (2026-03-10)
- **711 иконок** добавлены в основной набор (`icon_browser/icons-data.js`)
- **196 иконок** имеют обучающие данные в `icons_data/`
- Кандидаты для отбора: **~3493** иконок в `icon_browser/candidates-data.js`

---

## Флоу работы

### Шаг 1 — Пользователь выбирает иконки
Пользователь смотрит браузер (`icon_browser/index.html`) в режиме Candidates и выбирает список иконок для добавления в основной набор. Присылает список названий.

### Шаг 2 — Получить search terms из icons.json
```python
python3 -c "
import json
with open('icons.json') as f:
    data = json.load(f)
targets = ['anchor', 'bell', ...]  # список от пользователя
for key, val in data.items():
    label = val.get('label','')
    name = label.lower().replace(' ', '-')
    if name in targets:
        terms = val.get('search',{}).get('terms',[])
        uni = val.get('unicode','')
        print(f'{name} ({uni}): {terms}')
"
```

### Шаг 3 — Создать gen_icons скрипт с обучающими данными
Имя файла: `gen_icons_{N_start}_{N_end}.py` (нумерация по общему счётчику иконок).

**Текущий счётчик:** последний скрипт — `gen_icons_465_475.py`, следующий начинается с **476**.

Структура скрипта — строго по шаблону (см. раздел «Шаблон скрипта» ниже).

### Шаг 4 — Запустить скрипт
```bash
python3 gen_icons_NNN_MMM.py
```
Скрипт создаёт папки в `icons_data/{icon_name}/` с файлами:
- `train_en.csv`, `valid_en.csv`, `test_en.csv`
- `icon_log.json`

### Шаг 5 — Обновить icons-data.js и пересоздать candidates-data.js
```python
python3 << 'EOF'
import re, json

new_icons = [
    {"name": "anchor", "canonical": "anchor", "unicode": "f13d", "label": "Anchor", "alias": False},
    # ... остальные
]

# --- Обновить icons-data.js ---
with open('icon_browser/icons-data.js') as f:
    content = f.read()
match = re.search(r'window\.ICON_DATA\s*=\s*(\[[\s\S]*?\])\s*;?', content)
data = json.loads(match.group(1))
existing = {i['name'] for i in data}
added = [i for i in new_icons if i['name'] not in existing]
data.extend(added)
data.sort(key=lambda x: x['name'])

lines = ['// Auto-generated icon data for local browser\n// Created by Igor Djugostran\n\nwindow.ICON_DATA = [\n']
for i, icon in enumerate(data):
    comma = ',' if i < len(data) - 1 else ''
    lines.append(f'  {json.dumps(icon)}{comma}\n')
lines.append('];\n')
with open('icon_browser/icons-data.js', 'w') as f:
    f.writelines(lines)

# --- Пересоздать candidates-data.js ---
with open('icons.json') as f:
    raw = json.load(f)
processed = {i['name'] for i in data}
candidates = [
    {"name": v.get('label','').lower().replace(' ','-'), "unicode": v.get('unicode',''), "label": v.get('label','')}
    for v in raw.values()
    if v.get('label','').lower().replace(' ','-') not in processed
]
# Сортировка: 1 слово → 2 слова → 3 слова (по дефисам), внутри — алфавит
candidates.sort(key=lambda x: (len(x['name'].split('-')), x['name']))

# Построить IRRELEVANT_ICONS
with open('categories.yml') as f:
    yml = f.read()
IRRELEVANT_CATS = {'arrows','alphabet','numbers','punctuation-symbols','spinners','text-formatting','toggle','coding'}
irrelevant = set()
current_cat = None; in_block = False
for line in yml.splitlines():
    if re.match(r'^[a-z][\w-]+:$', line):
        current_cat = line[:-1]; in_block = False
    elif re.match(r'^  icons:$', line):
        in_block = True
    elif in_block and re.match(r'^    - ', line):
        if current_cat in IRRELEVANT_CATS:
            irrelevant.add(line.strip()[2:].strip().strip('"\''))
    elif re.match(r'^  [a-z]', line):
        in_block = False
for v in raw.values():
    if v.get('styles',[]) == ['brands']:
        irrelevant.add(v.get('label','').lower().replace(' ','-'))

out = ('// Auto-generated: core_ml_icons/icons.json minus current ICON_DATA\n'
       'window.IRRELEVANT_ICONS = new Set(' + json.dumps(sorted(irrelevant)) + ');\n'
       'window.CANDIDATE_DATA = ' + json.dumps(candidates) + ';\n')
with open('icon_browser/candidates-data.js', 'w') as f:
    f.write(out)

print(f"icons-data.js: {len(data)} icons (+{len(added)})")
print(f"candidates-data.js: {len(candidates)} candidates")
EOF
```

---

## Структура файлов проекта

```
core_ml_icons/
├── icons.json                     ← источник truth: все иконки + search terms + unicode
├── categories.yml                 ← категории для IRRELEVANT_ICONS фильтра
├── AGENT_CONTEXT.md               ← этот файл
│
├── icons_data/{icon_name}/        ← обучающие данные (63 иконки)
│   ├── train_en.csv
│   ├── valid_en.csv
│   ├── test_en.csv
│   └── icon_log.json
│
├── gen_icons_100_119.py           ← скрипты генерации (исторические + новые)
├── gen_icons_120_149.py
│   ... (до gen_icons_334_342.py)
│
└── icon_browser/
    ├── index.html                 ← браузер иконок
    ├── icons-data.js              ← window.ICON_DATA (578 иконок в наборе)
    └── candidates-data.js         ← window.IRRELEVANT_ICONS + window.CANDIDATE_DATA
```

### Важные файлы:
| Файл | Назначение |
|------|-----------|
| `icons.json` | Источник search terms и unicode для всех иконок |
| `icon_browser/icons-data.js` | Основной набор (добавленные иконки) |
| `icon_browser/candidates-data.js` | Кандидаты + фильтр нерелевантных |
| `icons_data/` | Обучающие данные по каждой иконке |

---

## Шаблон gen_icons скрипта

```python
#!/usr/bin/env python3
"""Generate English training data for icons NNN-MMM."""
from pathlib import Path
import csv, json

icons_dir = Path("icons_data")
icons_dir.mkdir(exist_ok=True)

def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "label"])
        w.writerows(rows)

def process_icon(icon, st_en, pst_en, reg_en, conv_en, typo_en, bnd_en, valid_en, test_en):
    icon_dir = icons_dir / icon
    icon_dir.mkdir(parents=True, exist_ok=True)
    train_en = [(t, icon) for t in st_en + pst_en + reg_en + conv_en + typo_en + bnd_en]
    write_csv(icon_dir / "train_en.csv", train_en)
    write_csv(icon_dir / "valid_en.csv", [(t, icon) for t in valid_en])
    write_csv(icon_dir / "test_en.csv",  [(t, icon) for t in test_en])
    log = {
        "icon": icon, "search_terms": st_en, "phrase_per_search_term": pst_en,
        "regular": reg_en, "conversational": conv_en, "typo": typo_en,
        "boundary": bnd_en, "valid": valid_en, "test": test_en,
    }
    with open(icon_dir / "icon_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    n_st = len(st_en); n_pst = len(pst_en)
    print(f"  {icon}: {len(train_en)} train rows  ({n_st} st + {n_pst} pst + 24)")

process_icon("anchor",
    st_en=["anchor", "boat", "dock", ...],   # из icons.json search.terms
    pst_en=[
        # 2 фразы на каждый term (итого len(st_en) × 2)
        "drop anchor in the harbor", "ship anchor holding vessel",
        ...
    ],
    reg_en=[
        # 10 естественных описательных фраз (visual / use-case / professional)
        ...
    ],
    conv_en=[
        # 4 разговорных фразы со стартером:
        # "I need a X icon for...", "add a X symbol to...",
        # "show a X for...", "use the X icon for..."
        ...
    ],
    typo_en=[
        # 4 реалистичных опечатки (перестановка букв, пропуск буквы, соседняя клавиша)
        ...
    ],
    bnd_en=[
        # 6 фраз описывающих ДРУГУЮ похожую иконку (для обучения различению)
        ...
    ],
    valid_en=["...", "...", "..."],   # 3 чистых фразы
    test_en=["...", "...", "..."],    # 3 чистых фразы
)
```

### Формула train rows:
```
train = len(st_en) + 2×len(st_en) + 10 reg + 4 conv + 4 typo + 6 bnd
      = 3×len(st_en) + 24
```

---

## Правила качества фраз

### search_terms (st_en)
- Берутся как есть из `icons.json`
- Пропускать: Unicode-имена в PascalCase ("Raised Hand"), явные опечатки ("uer"), дубли

### phrase_per_search_term (pst_en)
- **2 фразы на каждый термин** — НЕ повторение термина, а фраза с ним в контексте
- ❌ `"anchor anchor tool"` → ✅ `"drop anchor in the harbor"`

### regular (reg_en) — 10 фраз, минимум 3 разных структуры:
- **Visual**: как выглядит → `"heavy iron anchor with chain on the dock"`
- **Use-case**: для чего → `"anchor holding the vessel in the storm"`
- **Professional**: профессиональный контекст → `"HTML anchor tag for navigation links"`

### conversational (conv_en) — 4 фразы, всегда со стартером:
- `"I need a X icon for [context]"`
- `"add a X symbol to [screen]"`
- `"show a X for [feature]"`
- `"use the X icon for [section]"`

### typo (typo_en) — 4 реалистичных опечатки:
- Перестановка: `"ancor"` (пропуск h)
- Транспозиция: `"baot"` (o/a)
- Соседняя клавиша: `"ankhor"` (n→nk)

### boundary (bnd_en) — 6 фраз описывают ДРУГУЮ иконку:
- Выбрать 1–2 визуально похожих иконки и описать ИХ
- ❌ описывать ту же иконку → ✅ описывать hook/chain/buoy для anchor
- Иконки с похожими search_terms должны различаться через boundary

---

## Браузер иконок (icon_browser)

### Режимы:
- **List / Gallery** — просмотр основного набора (ICON_DATA)
- **Candidates** — просмотр кандидатов (CANDIDATE_DATA)

### Фильтр нерелевантных:
Чекбокс «Hide irrelevant icons» скрывает иконки из `IRRELEVANT_ICONS`:
- Категории: `arrows`, `alphabet`, `numbers`, `punctuation-symbols`, `spinners`, `text-formatting`, `toggle`, `coding`
- Бренды: иконки где `styles == ["brands"]`
- **Всего ~1244 нерелевантных иконок**

### Сортировка кандидатов:
По количеству слов в имени (дефис = разделитель), затем алфавит:
1. Одиночные слова: `acorn`, `alien`, `anchor`...
2. Двойные: `address-book`, `bell-on`...
3. Тройные: `album-circle-plus`...

### Обновление candidates-data.js:
Пересоздаётся каждый раз при добавлении иконок в ICON_DATA (Шаг 5).
Содержит `IRRELEVANT_ICONS` + `CANDIDATE_DATA`.

---

## Частые ошибки

| Ошибка | Правильно |
|--------|-----------|
| Брать search terms из icons.claude.json | Брать из **icons.json** |
| Забыть пересоздать candidates-data.js | Всегда выполнять Шаг 5 после добавления |
| Не сохранить IRRELEVANT_ICONS при пересоздании | Всегда включать в candidates-data.js |
| Нарушить сортировку кандидатов | `sort(key=lambda x: (len(x['name'].split('-')), x['name']))` |
| boundary описывает ту же иконку | boundary = описание ДРУГОЙ похожей иконки |
| Механическое повторение в pst | `"anchor anchor"` — плохо, нужен контекст |

#!/usr/bin/env python3
"""Supplement for batch 001: top up icons that didn't quite reach 60 EN rows."""

import csv
from pathlib import Path

icons_dir = Path("icons")


def read_texts(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return [r["text"].strip() for r in csv.DictReader(f)]


def append_csv(path, rows):
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)


def expand(icon, new_en, new_ru):
    assert len(new_en) == len(new_ru), f"{icon}: EN={len(new_en)} RU={len(new_ru)} mismatch"
    en_path = icons_dir / icon / "train_en.csv"
    ru_path = icons_dir / icon / "train_ru.csv"
    existing_en = set(read_texts(en_path))
    existing_ru = set(read_texts(ru_path))
    add_en = [(t, icon) for t in new_en if t not in existing_en]
    add_ru = [(t, icon) for t in new_ru if t not in existing_ru]
    append_csv(en_path, add_en)
    append_csv(ru_path, add_ru)
    total_en = len(existing_en) + len(add_en)
    total_ru = len(existing_ru) + len(add_ru)
    print(f"  {icon}: +{len(add_en)} EN  +{len(add_ru)} RU  (total EN={total_en} RU={total_ru})")


# ── tablet (57 → 60) ────────────────────────────────────────────────────────
expand("tablet",
    new_en=[
        "watch shows on the tablet tonight",
        "transfer photos from the tablet to the computer",
        "clean the tablet screen with a microfiber cloth",
    ],
    new_ru=[
        "смотреть сериалы на планшете вечером",
        "перенести фото с планшета на компьютер",
        "протереть экран планшета салфеткой",
    ],
)

# ── tank-water (57 → 60) ────────────────────────────────────────────────────
expand("tank-water",
    new_en=[
        "hire a plumber to fix the tank",
        "water tank sensor reading is off",
        "add a filter to the rainwater tank",
    ],
    new_ru=[
        "вызвать сантехника починить бак",
        "датчик бака показывает неправильно",
        "поставить фильтр на бак дождевой воды",
    ],
)

# ── vest-patches (57 → 60) ──────────────────────────────────────────────────
expand("vest-patches",
    new_en=[
        "display the patches on the denim vest",
        "hand-stitch the patch with heavy thread",
        "add the new band patch to the back panel",
    ],
    new_ru=[
        "разместить нашивки на джинсовом жилете",
        "вручную пришить нашивку толстой нитью",
        "добавить новую нашивку группы на спину",
    ],
)

# ── wheelchair (57 → 60) ────────────────────────────────────────────────────
expand("wheelchair",
    new_en=[
        "check wheelchair accessible entrances at the venue",
        "inflate the wheelchair tires before the outing",
        "adjust the wheelchair seat height",
    ],
    new_ru=[
        "проверить доступные входы для колясок на месте",
        "накачать шины коляски перед прогулкой",
        "настроить высоту сиденья коляски",
    ],
)

# ── window (57 → 60) ────────────────────────────────────────────────────────
expand("window",
    new_en=[
        "snap the window to the left side",
        "switch between open windows quickly",
        "tile all windows on the screen",
    ],
    new_ru=[
        "привязать окно к левой стороне",
        "быстро переключаться между окнами",
        "разложить все окна плиткой",
    ],
)

# ── moped (57 → 60) ─────────────────────────────────────────────────────────
expand("moped",
    new_en=[
        "replace the moped brake pads",
        "check moped tire pressure this morning",
        "take the moped for a test ride",
    ],
    new_ru=[
        "заменить тормозные колодки мопеда",
        "проверить давление в шинах мопеда",
        "прокатиться на мопеде на пробу",
    ],
)

# ── stairs (57 → 60) ────────────────────────────────────────────────────────
expand("stairs",
    new_en=[
        "count flights of stairs for the fitness tracker",
        "replace the stair light bulb",
        "sweep the front porch steps",
    ],
    new_ru=[
        "считать лестничные пролёты для фитнес-трекера",
        "заменить лампочку на лестнице",
        "подмести ступеньки крыльца",
    ],
)

# ── cucumber (57 → 60) ──────────────────────────────────────────────────────
expand("cucumber",
    new_en=[
        "pick cucumbers from the garden today",
        "cucumber salad for the barbecue side dish",
        "spiralize the cucumber for the noodle bowl",
    ],
    new_ru=[
        "собрать огурцы с грядки сегодня",
        "огуречный салат к шашлыку",
        "нарезать огурец спиралью для салата",
    ],
)

print("\nSupplement done. Run merge and audit next.")

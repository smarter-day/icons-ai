#!/usr/bin/env python3
"""Remove curated ambiguous one-term train rows from icon datasets."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"

AMBIGUOUS_TERMS = {
    "en": {
        "travel": set(),
        "music": {"music"},
        "vehicle": set(),
        "holiday": set(),
        "tool": set(),
        "currency": set(),
        "fauna": set(),
        "modify": set(),
        "storage": set(),
        "computer": {"computer"},
        "animal": set(),
        "game": set(),
        "building": {"building"},
        "food": set(),
        "halloween": set(),
        "transportation": set(),
        "money": set(),
        "mammal": set(),
        "maintenance": set(),
        "location": set(),
        "navigation": set(),
        "signal": set(),
        "notification": set(),
        "settings": {"gear"},
        "sandwich": {"sandwich"},
        "salary": set(),
        "purchase": set(),
        "paper": set(),
        "map": {"map"},
        "knowledge": set(),
        "instrument": set(),
        "fall": set(),
        "xmas": set(),
        "christmas": set(),
        "auto": set(),
        "alert": set(),
        "record": set(),
        "furniture": set(),
        "clothing": set(),
    },
    "ru": {
        "инструмент": set(),
        "праздник": set(),
        "путешествие": set(),
        "животное": set(),
        "валюта": set(),
        "фауна": set(),
        "изменить": set(),
        "хранение": set(),
        "транспортное средство": set(),
        "музыка": {"music"},
        "компьютер": {"computer"},
        "оборудование": set(),
        "млекопитающее": set(),
        "игра": set(),
        "деньги": set(),
        "машина": set(),
        "карта": {"map"},
        "здание": {"building"},
        "транспорт": set(),
        "инвентарь": set(),
        "дизайн": set(),
        "спорт": set(),
        "местоположение": set(),
        "купить": set(),
        "искусство": set(),
        "завтрак": set(),
        "еда": set(),
        "архив": set(),
        "покупка": set(),
        "одежда": set(),
        "настройки": {"gear"},
        "навигация": set(),
        "зарплата": set(),
        "доставка": set(),
        "хэллоуин": set(),
        "фэнтези": set(),
        "уведомление": set(),
        "сигнал": set(),
        "оружие": set(),
        "оплата": set(),
        "здоровье": set(),
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def clean_language(lang: str) -> dict[str, object]:
    summary: dict[str, object] = {"language": lang, "icons_changed": 0, "rows_removed": 0, "changes": []}
    terms = AMBIGUOUS_TERMS[lang]

    for icon_dir in sorted(path for path in ICONS_DIR.iterdir() if path.is_dir()):
        icon = icon_dir.name
        path = icon_dir / f"train_{lang}.csv"
        if not path.exists():
            continue

        rows = read_rows(path)
        filtered = []
        removed_terms: list[str] = []

        for row in rows:
            text = row["text"].strip()
            keepers = terms.get(text)
            if keepers is not None and icon not in keepers:
                removed_terms.append(text)
                continue
            filtered.append(row)

        if len(filtered) == len(rows):
            continue

        write_rows(path, filtered)
        summary["icons_changed"] += 1
        summary["rows_removed"] += len(rows) - len(filtered)
        summary["changes"].append(
            {
                "icon": icon,
                "removed_count": len(rows) - len(filtered),
                "removed_terms": removed_terms,
            }
        )

    return summary


def main() -> None:
    report = {
        "en": clean_language("en"),
        "ru": clean_language("ru"),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

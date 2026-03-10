#!/usr/bin/env python3
"""Fill missing Russian CSV datasets from existing English CSV files."""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Iterable

import requests


ROOT = Path(__file__).resolve().parents[1]
ICONS_DIR = ROOT / "icons"
SPLITS = ("train", "valid", "test")
CACHE_PATH = ROOT / "scripts" / ".ru_translation_cache.json"


def read_rows(path: Path) -> list[tuple[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [(row["text"], row["label"]) for row in reader]


def write_rows(path: Path, rows: Iterable[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)


def load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    with CACHE_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache: dict[str, str]) -> None:
    with CACHE_PATH.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2, sort_keys=True)


def translate_batch(texts: list[str], session: requests.Session) -> list[str]:
    url = "https://translate.googleapis.com/translate_a/single"
    joined = "\n".join(texts)
    params = {
        "client": "gtx",
        "sl": "en",
        "tl": "ru",
        "dt": "t",
        "q": joined,
    }
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    translated = "".join(part[0] for part in payload[0] if part and part[0] is not None)
    return [line.strip() for line in translated.split("\n")]


def populate_cache(texts: list[str], cache: dict[str, str], session: requests.Session) -> None:
    pending = [text for text in dict.fromkeys(texts) if text and text not in cache]
    batch_size = 40
    for i in range(0, len(pending), batch_size):
        batch = pending[i : i + batch_size]
        attempts = 3
        for attempt in range(1, attempts + 1):
            try:
                translated = translate_batch(batch, session)
                if len(translated) != len(batch):
                    raise ValueError("Translation batch size mismatch")
                for source, target in zip(batch, translated):
                    cache[source] = target or source
                save_cache(cache)
                break
            except Exception:
                if attempt == attempts:
                    for source in batch:
                        cache[source] = source
                    save_cache(cache)
                else:
                    time.sleep(1.5 * attempt)
        time.sleep(0.2)


def main() -> None:
    missing_files: list[tuple[Path, Path]] = []

    for icon_dir in sorted(path for path in ICONS_DIR.iterdir() if path.is_dir()):
        for split in SPLITS:
            en_path = icon_dir / f"{split}_en.csv"
            ru_path = icon_dir / f"{split}_ru.csv"
            if en_path.exists() and not ru_path.exists():
                missing_files.append((en_path, ru_path))

    if not missing_files:
        print("No missing Russian CSV files found.")
        return

    cache = load_cache()
    session = requests.Session()

    for index, (en_path, ru_path) in enumerate(missing_files, start=1):
        rows = read_rows(en_path)
        populate_cache([text for text, _ in rows], cache, session)
        translated_rows = [(cache.get(text, text), label) for text, label in rows]
        write_rows(ru_path, translated_rows)
        print(f"[{index}/{len(missing_files)}] {ru_path.relative_to(ROOT)}", flush=True)

    print(f"Created {len(missing_files)} files.")


if __name__ == "__main__":
    main()

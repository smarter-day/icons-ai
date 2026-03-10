#!/usr/bin/env python3
"""Deprecated: automatic Russian dataset generation is no longer allowed."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = ROOT / "docs" / "icon-dataset-editorial-guide.md"


def main() -> None:
    raise SystemExit(
        "Automatic RU generation is disabled by repository policy.\n"
        f"Use the manual bilingual workflow documented in {GUIDE_PATH.relative_to(ROOT)}\n"
        "and run scripts/audit_icon_dataset.py to find missing Russian files."
    )


if __name__ == "__main__":
    main()

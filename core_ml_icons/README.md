# core_ml_icons

A dataset collection for training a Core ML text classifier that maps text descriptions to icons.

## Structure

- `icons/` - main per-icon dataset collection, one folder per icon
- `icons/<icon>/train_en.csv`, `valid_en.csv`, `test_en.csv` - train/valid/test files for a single icon
- `icons/<icon>/train_ru.csv`, `valid_ru.csv`, `test_ru.csv` - synchronized Russian train/valid/test files
- `scripts/merge_icon_datasets.py` - script that merges all icons into one combined dataset
- `scripts/audit_icon_dataset.py` - dataset audit for bilingual sync, leakage, and weak coverage
- `docs/icon-semantic-groups.yml` - semantic conflict groups for manual disambiguation work
- `docs/icon-semantic-coverage.json` - full per-icon semantic coverage: grouped, pair-risk, isolated
- `merged_icons_dataset/` - output folder for merged Core ML CSV files
- `MyTextClassifier.mlproj/` - Core ML project

## Editorial policy

Dataset growth is manual-first:

- no automatic expression generation
- no automatic machine translation as final dataset content
- English and Russian rows must be added together
- every expression must be meaningful and reviewed by a human
- phrases should primarily model task titles, short task intents, and real user queries
- visual icon descriptions are allowed only as a secondary support layer

Detailed rules live in `docs/icon-dataset-editorial-guide.md`.
Conflict groups live in `docs/icon-semantic-groups.yml`.
Full coverage for all icons lives in `docs/icon-semantic-coverage.json`.

## Audit the dataset

Run the audit before merging or extending datasets:

```bash
python3 scripts/audit_icon_dataset.py
```

Emit the full report as JSON:

```bash
python3 scripts/audit_icon_dataset.py --json
```

Rebuild semantic coverage after changing conflict groups:

```bash
python3 scripts/build_semantic_coverage.py
```

## Build the combined dataset

The script automatically scans all folders inside `icons/` and merges the datasets into 3 combined files:

- `train_en.csv`
- `valid_en.csv`
- `test_en.csv`

Run:

```bash
python3 scripts/merge_icon_datasets.py
```

The output files will be written to `merged_icons_dataset/`.

By default, the script:

- reads data from `icons/`
- merges only complete icon datasets that contain `train`, `valid`, and `test`
- shuffles rows deterministically
- creates `merge_summary_en.json` with row counts and the merged icon list

## Additional options

Build the Russian dataset:

```bash
python3 scripts/merge_icon_datasets.py --lang ru
```

Use a different output directory:

```bash
python3 scripts/merge_icon_datasets.py --output-dir custom_dataset
```

Keep the original row order:

```bash
python3 scripts/merge_icon_datasets.py --no-shuffle
```

Skip incomplete icon folders:

```bash
python3 scripts/merge_icon_datasets.py --allow-missing
```

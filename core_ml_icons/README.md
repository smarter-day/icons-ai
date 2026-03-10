# core_ml_icons

A dataset collection for training a Core ML text classifier that maps text descriptions to icons.

## Structure

- `icons/` - main per-icon dataset collection, one folder per icon
- `icons/<icon>/train_en.csv`, `valid_en.csv`, `test_en.csv` - train/valid/test files for a single icon
- `scripts/merge_icon_datasets.py` - script that merges all icons into one combined dataset
- `merged_icons_dataset/` - output folder for merged Core ML CSV files
- `MyTextClassifier.mlproj/` - Core ML project

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

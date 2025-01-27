#!/bin/zsh

echo "Categorizing 3276 icons..."
./main.py categorize-icons \
  --input-icons data/icons.json \
  --output-filtered data/filtered_icons_3276.json \
  --output-keywords data/keywords.json \
  --categories data/categories.json \
  --limit 3276 \
  --chunk-size 80 \
  --languages en,ru \
  --translator openai || exit 1

echo "Building previews..."
./main.py preview --input-icons data/filtered_icons_3276.json --output-html data/preview_3276.html || exit 1

echo "Done."

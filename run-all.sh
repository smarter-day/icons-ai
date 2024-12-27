#!/bin/zsh

echo "Categorizing 250 icons..."
./main.py categorize-icons \
  --input-icons data/icons.json \
  --output-filtered data/filtered_icons_250.json \
  --output-keywords data/keywords_250.json \
  --categories data/categories.json \
  --limit 250 \
  --chunk-size 90 \
  --languages en,ru \
  --translator openai || exit 1

echo "Copying keywords from 250 to 500..."
cp data/keywords_250.ru.json data/keywords_500.ru.json || exit 1

echo "Categorizing 500 icons..."
./main.py categorize-icons \
  --input-icons data/icons.json \
  --output-filtered data/filtered_icons_500.json \
  --output-keywords data/keywords_500.json \
  --categories data/categories.json \
  --limit 500 \
  --chunk-size 90 \
  --languages en,ru \
  --translator openai || exit 1

echo "Copying keywords from 500 to 1000..."
cp data/keywords_500.ru.json data/keywords_1000.ru.json || exit 1

echo "Categorizing 1000 icons..."
./main.py categorize-icons \
  --input-icons data/icons.json \
  --output-filtered data/filtered_icons_1000.json \
  --output-keywords data/keywords_1000.json \
  --categories data/categories.json \
  --limit 1000 \
  --chunk-size 90 \
  --languages en,ru \
  --translator openai || exit 1

echo "Building previews..."
./main.py preview --input-icons data/filtered_icons_250.json --output-html data/preview-250.html || exit 1
./main.py preview --input-icons data/filtered_icons_500.json --output-html data/preview-500.html || exit 1
./main.py preview --input-icons data/filtered_icons_1000.json --output-html data/preview-1000.html || exit 1

echo "Done."

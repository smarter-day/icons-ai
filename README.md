# Icons AI

Icons AI is a powerful command-line tool designed to streamline the process of organizing and managing icon sets. It leverages artificial intelligence to generate categories, categorize icons, extract keywords, and even translate those keywords into different languages. This tool is perfect for designers, developers, and anyone working with large icon libraries who need an efficient way to organize and search through their collections.

Key features:
- Generate meaningful categories for icon sets
- Automatically categorize icons based on AI-generated categories
- Extract relevant keywords from icons
- Translate keywords into multiple languages
- Utilizes local LLM (Large Language Model) for enhanced privacy and offline capabilities

Whether you're managing a small icon set or a vast library, Icons AI provides the tools you need to keep your icons organized, searchable, and easily accessible.

## Software Used

Icons AI leverages several powerful tools and libraries to provide its functionality:

### AI and Machine Learning
- **Local LLM (Large Language Model)**: We use a locally-run LLM for generating categories, categorizing icons, and extracting keywords. This ensures privacy and allows for offline operation.
- **Hugging Face Transformers**: Likely used for running the local LLM and for various NLP tasks.

### Translation
- **Argos Translate**: An open-source neural machine translation library, used for translating keywords into multiple languages without relying on external APIs.

The specific versions and additional dependencies can be found in the `requirements.txt` file.

## Usage

### Requirements

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Models

Download local LLM models:

```bash
./download-models.sh
```

### Help

```bash
./main.py --help
```

### Step 1: Generate Categories

```bash
./main.py generate-categories --output data/categories.json
```

### Step 2: Categorize Icons

**250 icons**

```bash
./main.py categorize-icons \
    --input-icons data/icons.json \
    --output-filtered data/filtered_icons_250.json \
    --output-keywords data/keywords_250.json \
    --categories data/categories.json \
    --limit 250 \
    --chunk-size 90 \
    --languages en,ru \
    --translator openai
```

**500 icons**

```bash
./main.py categorize-icons \
    --input-icons data/icons.json \
    --output-filtered data/filtered_icons_500.json \
    --output-keywords data/keywords_500.json \
    --categories data/categories.json \
    --limit 500 \
    --chunk-size 90 \
    --languages en,ru \
    --translator openai
```

**1000 icons**

```bash
./main.py categorize-icons \
    --input-icons data/icons.json \
    --output-filtered data/filtered_icons_1000.json \
    --output-keywords data/keywords_1000.json \
    --categories data/categories.json \
    --limit 1000 \
    --chunk-size 90 \
    --languages en,ru \
    --translator openai
```

### Step 3: Preview

**250 icons**

```bash
./main.py preview --input-icons data/filtered_icons_250.json --output-html data/preview-250.html
```

**500 icons**

```bash
./main.py preview --input-icons data/filtered_icons_500.json --output-html data/preview-500.html
```

**1000 icons**

```bash
./main.py preview --input-icons data/filtered_icons_1000.json --output-html data/preview-1000.html
```

### Additional Step: Translate Keywords

If you have categories and existing translations and just need to translate to additional languages, use just this command.

```bash
./main.py translate-keywords --source data/keywords.json --output data/keywords.json --languages ru
```

## Environment

1. Take openai secret from google secrets in production env.


## Licence

Private, belongs to smarter.day

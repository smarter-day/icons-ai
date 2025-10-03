# Icons AI System

A comprehensive system for processing, categorizing, translating, and creating embeddings for icon datasets with multi-language support.

## System Overview

This system takes a collection of icons with English tags and processes them through a pipeline that:

1. Strips and cleans the icon data
2. Enhances English tags with synonyms
3. **Categorizes icons** using AI to identify daily-life relevant icons
4. Translates tags to multiple languages using AI (only for relevant icons)
5. Creates language-specific icon files (only relevant icons)
6. Generates embeddings for search and similarity (only relevant icons)

## Architecture

The system is built around a **project-based configuration** approach where all settings are defined in YAML files. Each script can be run independently or as part of a complete workflow.

### Core Components

- **Configuration System**: Centralized settings in `projects/v1.yaml`
- **Library Modules**: Reusable components in `library/`
- **Processing Scripts**: Specialized tools for each workflow step
- **Data Pipeline**: Sequential processing from raw icons to final outputs

## Workflow

### 1. Prepare Models

```bash
python prepare_models.py
```

Downloads and prepares FastText language models for the configured languages. See `projects/v1.yaml` for model settings.

### 2. Strip English Icons

```bash
python strip_english_icons.py
```

Creates a clean, stripped version of the English icons containing only essential fields (name and tags). This becomes the base file for all subsequent processing.

### 3. Generate Synonyms (Optional)

```bash
python generate_synonims.py
```

Enhances the English stripped icons by adding synonyms to each tag using NLTK WordNet. This increases the vocabulary for better translation coverage.

### 4. Categorize Icons

```bash
python categorize_icons.py
```

**NEW**: Uses AI to categorize icons into daily-life relevant categories. Only icons that match daily-life activities are marked as "enabled". This step creates:

- `data/icons.enabled.en.json` - Only relevant icons
- `data/categories.json` - Category assignments for each icon

**Categories**: See the 15 predefined categories in `categorize_icons.py` (Family, Work, Health, etc.)

### 5. Translate Keywords

```bash
python translate_keywords.py --languages ru,fr
```

Translates unique tags from **enabled icons only** into target languages using OpenAI. Creates translation dictionaries (`data/keywords.{language}.json`) for each language.

### 6. Translate Icons

```bash
python translate_icons.py --languages ru,fr
```

Uses the translation dictionaries to create language-specific icon files. **Only processes enabled icons** - creates smaller, focused files with translated tags.

### 7. Create Embeddings

```bash
python create_icons_embeddings.py --languages en,ru,fr
```

Generates embeddings for **enabled icons only** in each language. Creates searchable vector representations for the most relevant icons.

## Configuration

All system behavior is controlled through the project configuration file. See `projects/v1.yaml` for:

- **Models**: FastText model settings and dimensions
- **Icons**: File paths and naming patterns
- **Translation**: OpenAI settings and parameters
- **Languages**: Supported languages and their specific settings

### Environment Variables

Set these in your `.env` file:

- `DEFAULT_PROJECT`: Path to default project YAML file
- `OPENAI_API_KEY`: Your OpenAI API key for translations

## File Structure

```
data/
├── icons.json                    # Original icon dataset
├── icons.stripped.en.json        # Stripped English icons (all icons)
├── icons.enabled.en.json         # Only relevant icons (categorized)
├── icons.stripped.{lang}.json    # Translated icon files (enabled only)
├── keywords.{lang}.json          # Translation dictionaries
└── categories.json              # Icon category assignments

embeddings/
├── icon_embeddings.{lang}.json   # Icon vector embeddings (enabled only)
└── vocab_embeddings.{lang}.json  # Vocabulary embeddings

.models/
└── v1/                          # FastText language models
```

## Usage Patterns

### Complete Workflow

Run all steps in sequence for a full processing pipeline:

```bash
python prepare_models.py
python strip_english_icons.py
python generate_synonims.py
python categorize_icons.py                    # NEW: Categorize icons
python translate_keywords.py --languages ru,fr
python translate_icons.py --languages ru,fr
python create_icons_embeddings.py --languages en,ru,fr
```

**Or use the automated script:**

```bash
./run-all.sh
```

### Single Language Processing

Process only specific languages by using the `--languages` parameter:

```bash
python translate_keywords.py --languages ru
python translate_icons.py --languages ru
```

### Custom Configuration

Use different project settings:

```bash
python translate_keywords.py --project projects/custom.yaml --languages ru
```

## Categorization System

The system uses AI-powered categorization to identify icons relevant to daily life activities. Icons are classified into 15 predefined categories:

**Categories** (see `categorize_icons.py` for full list):

- Family and Relationships
- Friends and Social  
- Work and Career
- Health and Fitness
- Finance and Money
- Education and Learning
- Shopping and Errands
- Travel and Transportation
- Home and Chores
- Food and Cooking
- Hobbies and Entertainment
- Pets and Animals
- Events and Calendar
- Personal Care
- Technology and Gadgets

**Configuration**: Categorization threshold and model can be adjusted in `projects/v1.yaml` under `models.defaults.categorization`.

**Output**:

- `data/icons.enabled.en.json` - Only relevant icons
- `data/categories.json` - Category assignments for each icon

## Key Features

- **Smart Categorization**: AI-powered filtering to focus on relevant icons
- **Project-Based Configuration**: All settings centralized in YAML files
- **Language Support**: Process multiple languages with language-specific settings
- **AI-Powered Translation**: Uses OpenAI for high-quality tag translation
- **Embedding Generation**: Creates searchable vector representations
- **Modular Design**: Each script can be run independently
- **Error Handling**: Graceful handling of missing files and API failures
- **Progress Tracking**: Visual progress bars for long-running operations

## Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Key dependencies include:

- FastText for language models and embeddings
- OpenAI for AI-powered translations
- NLTK for English synonym generation
- Typer for command-line interfaces

## Workflow Benefits

The categorization-first approach provides several advantages:

- **🎯 Quality Focus**: Only relevant icons get expensive translation and embedding processing
- **💰 Cost Efficiency**: Reduces translation API calls by ~57% (typically 1400 vs 3300 icons)
- **⚡ Performance**: Faster embedding generation with fewer icons
- **🌍 Clean Datasets**: Language files contain only relevant, translated icons
- **📊 Smart Filtering**: AI determines relevance based on daily-life categories

## Output Files

The system generates several types of output files:

- **Stripped Icons**: Clean, minimal icon data (all icons)
- **Enabled Icons**: Only relevant icons after categorization
- **Translation Files**: Keyword mappings for each language (enabled icons only)
- **Translated Icons**: Language-specific icon collections (enabled icons only)
- **Embeddings**: Vector representations for search and similarity (enabled icons only)
- **Categories**: Icon-to-category assignments for analysis

Each file type follows consistent naming patterns with language placeholders, making it easy to work with multiple languages programmatically.

## Getting Started

1. Configure your project settings in `projects/v1.yaml`
2. Set up your `.env` file with required API keys
3. Run the workflow steps in sequence
4. Use the generated files for your application needs

The system is designed to be flexible and extensible, allowing you to customize the processing pipeline based on your specific requirements.

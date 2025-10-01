# Icons AI System

A comprehensive system for processing, translating, and creating embeddings for icon datasets with multi-language support.

## System Overview

This system takes a collection of icons with English tags and processes them through a pipeline that:
1. Strips and cleans the icon data
2. Enhances English tags with synonyms
3. Translates tags to multiple languages using AI
4. Creates language-specific icon files
5. Generates embeddings for search and similarity

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

### 4. Translate Keywords
```bash
python translate_keywords.py --languages ru,fr
```
Translates all unique tags from the English stripped icons into target languages using OpenAI. Creates translation dictionaries (`data/keywords.{language}.json`) for each language.

### 5. Translate Icons
```bash
python translate_icons.py --languages ru,fr
```
Uses the translation dictionaries to create language-specific icon files. Each icon's tags are translated while preserving the original structure.

### 6. Create Embeddings
```bash
python create_icons_embeddings.py --languages en,ru,fr
```
Generates FastText embeddings for both individual icons and vocabulary words in each language. Creates searchable vector representations.

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
├── icons.stripped.en.json        # Stripped English icons
├── icons.stripped.{lang}.json    # Translated icon files
└── keywords.{lang}.json          # Translation dictionaries

embeddings/
├── icon_embeddings.{lang}.json   # Icon vector embeddings
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
python translate_keywords.py --languages ru,fr
python translate_icons.py --languages ru,fr
python create_icons_embeddings.py --languages en,ru,fr
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

## Key Features

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

## Output Files

The system generates several types of output files:
- **Stripped Icons**: Clean, minimal icon data
- **Translation Files**: Keyword mappings for each language
- **Translated Icons**: Language-specific icon collections
- **Embeddings**: Vector representations for search and similarity

Each file type follows consistent naming patterns with language placeholders, making it easy to work with multiple languages programmatically.

## Getting Started

1. Configure your project settings in `projects/v1.yaml`
2. Set up your `.env` file with required API keys
3. Run the workflow steps in sequence
4. Use the generated files for your application needs

The system is designed to be flexible and extensible, allowing you to customize the processing pipeline based on your specific requirements.
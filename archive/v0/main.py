#!.venv/bin/python
import hashlib
import json
import math
import os
import re
import time
from collections import defaultdict
from pathlib import Path

import dotenv
import numpy as np
import torch
import typer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util

MAX_SYNONYMS = 3
languages = {
    "en": "ENGLISH",
    "zh": "MANDARIN CHINESE",
    "hi": "HINDI",
    "es": "SPANISH",
    "fr": "FRENCH",
    "ar": "ARABIC",
    "bn": "BENGALI",
    "pt": "PORTUGUESE",
    "ru": "RUSSIAN",
    "ja": "JAPANESE",
    "de": "GERMAN",
    "ko": "KOREAN",
    "vi": "VIETNAMESE",
    "tr": "TURKISH",
    "it": "ITALIAN",
    "ur": "URDU",
    "fa": "PERSIAN",
    "sw": "SWAHILI",
    "ta": "TAMIL",
    "th": "THAI",
    "nl": "DUTCH",
    "pl": "POLISH",
    "ms": "MALAY",
    "id": "INDONESIAN",
    "tl": "TAGALOG",
    "uk": "UKRAINIAN",
    "ha": "HAUSA",
    "my": "BURMESE",
    "he": "HEBREW",
    "am": "AMHARIC",
    "pa": "PUNJABI",
}

dotenv.load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise typer.Exit(code=1)

app = typer.Typer()

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def calculate_median_threshold(categorized_icons: dict, min_score: float):
    all_scores = [
        icon["match_score"]
        for icons in categorized_icons.values()
        for icon in icons
        if icon["match_score"] >= min_score
    ]
    return np.median(all_scores) if all_scores else min_score


def distribute_icons(categorized_icons, total_limit=250, min_score=0.0, max_per_category=0):
    # Calculate dynamic relevance threshold
    if min_score > 0.0:
        relevance_threshold = calculate_median_threshold(categorized_icons, min_score)
    else:
        relevance_threshold = 0.0

    # Filter icons by threshold and sort by match score
    filtered_icons = {
        category: sorted(
            [icon for icon in icons if icon["match_score"] >= relevance_threshold],
            key=lambda x: x["match_score"],
            reverse=True,
        )
        for category, icons in categorized_icons.items()
    }

    total_categories = len(filtered_icons)
    if max_per_category != 0:
        max_per_category = total_limit // total_categories
    else:
        max_per_category = total_limit
    distributed_icons = []
    # Distribute icons round-robin for better balance
    for i in range(max_per_category):
        for category in filtered_icons.keys():
            if len(filtered_icons[category]) > i:
                distributed_icons.append(filtered_icons[category][i])

    return distributed_icons


def preprocess_text(text):
    words = text.split()
    processed = [
        lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words
    ]
    return " ".join(processed)


def categorize_icon_semantic(icon_tags, categories, model):
    best_category = None
    highest_score = float("-inf")
    category_scores = {}

    # Preprocess and encode icon description
    icon_description = preprocess_text(" ".join(t.strip().lower() for t in icon_tags.split(",") if t.strip()))
    icon_embedding = model.encode(icon_description, convert_to_tensor=True)

    # Iterate through new category structure
    for category, cat_data in categories.items():
        # Use the keywords list from the category data
        cat_keywords = cat_data.get("keywords", [])
        category_description = preprocess_text(" ".join(cat_keywords))
        category_embedding = model.encode(category_description, convert_to_tensor=True)
        score = util.pytorch_cos_sim(icon_embedding, category_embedding).item()
        category_scores[category] = score
        if score > highest_score:
            highest_score = score
            best_category = category

    return best_category, highest_score, category_scores


def extract_base_name_and_version(name):
    match = re.match(r'^(.*?)(?:-(\d+))*$', name)
    if match:
        base_name = match.group(1)
        versions = [int(num) for num in re.findall(r'-(\d+)', name)]
        return base_name, versions
    return name, []


def filter_duplicates(icons):
    grouped_icons = defaultdict(list)
    for icon in icons:
        base_name, versions = extract_base_name_and_version(icon['name'])
        grouped_icons[base_name].append((icon, versions))
    filtered_icons = []
    for base_name, group in grouped_icons.items():
        sorted_group = sorted(group, key=lambda x: (x[1], len(x[1])))
        filtered_icons.append(sorted_group[0][0])
    return filtered_icons


def load_icons_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return filter_duplicates(data.get("icons", []))


def load_categories_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_synonyms_for_word(word, max_synonyms=MAX_SYNONYMS):
    synonyms = set()
    word_synsets = wn.synsets(word)
    if not word_synsets:
        return set()
    primary_synset = word_synsets[0]
    for syn in word_synsets:
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            if synonym != word:
                similarity = primary_synset.wup_similarity(syn)
                if similarity is not None:
                    synonyms.add((synonym, similarity))
    sorted_synonyms = sorted(synonyms, key=lambda x: x[1], reverse=True)
    top_synonyms = {synonym for synonym, _ in sorted_synonyms[:max_synonyms]}
    return top_synonyms


def enrich_keywords(keywords):
    keyword_list = [kw.strip().lower() for kw in keywords.split(",") if kw.strip()]
    all_keywords = set(keyword_list)
    for keyword in keyword_list:
        syns = get_synonyms_for_word(keyword)
        all_keywords.update(syns)
    return sorted(all_keywords)


def openai_chat(prompt, api_key, model="gpt-4o", max_tokens=1024, temperature=0.7):
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()


@app.command()
def generate_categories(
    output: str = typer.Option(..., help="Path to save generated categories JSON"),
):
    prompt = """Here’s a flat list of 10 well-organized categories with enough details:

- Tasks & Productivity: Actions, tasks, to-dos, reminders, projects, goals, habits, stress management, and self-care.  
- Time & Organization: Time, date, location, calendar, scheduling, events, and group activities.  
- People & Relationships: People, relationships, networking, teamwork, social media, and collaboration.  
- Communication & Media: Communication, video, audio, music, podcasts, streaming, and meeting tools.  
- Finance & Commerce: Finance, banking, investments, loans, credit cards, shopping, sales, expenses, and revenue management.  
- Learning & Growth: Learning, studying, growth, motivation, emotional intelligence, research, analysis, and reporting.  
- Health & Well-being: Health, fitness, nutrition, exercise, sleep, mental health, and personal well-being.  
- Travel & Logistics: Travel, navigation, transportation, driving, and logistics management.  
- Technology & Creativity: Technology, tools, design, photography, art, architecture, gaming, and entertainment.  
- Home & Maintenance: Home maintenance, repairs, cleaning, recycling, waste management, and inventory organization.    

For each category, give me a short descriptive name and then an object containing an "audience" (list of unified slugs) and a "keywords" array with 20 unique keywords.
Return the data in strict JSON format without extra commentary, markdown formatting or any other additions. Only raw json:
{
  "<Shortened Category Name>": {
    "audience": ["slug1", "slug2", ...],
    "keywords": ["keyword1", "keyword2", ...]
  },
  ...
}
    """
    response = openai_chat(prompt, api_key=openai_api_key, model="gpt-4o", max_tokens=8000, temperature=0.8)
    try:
        print(response)
        categories_data = json.loads(response)
    except json.JSONDecodeError:
        typer.echo("Failed to parse OpenAI response as JSON. Please refine the prompt or check the response.")
        return

    with open(output, "w", encoding="utf-8") as f:
        json.dump(categories_data, f, ensure_ascii=False, indent=2)

    typer.echo(f"Categories generated and saved to {output}.")


def chunk_list(input_list, chunk_size):
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i:i + chunk_size]


def categorize_icon_llm(icon_tags, categories, model, tokenizer):
    icon_description = " ".join(t.strip().lower() for t in icon_tags.split(",") if t.strip())
    best_category = None
    highest_score = float("-inf")
    category_scores = {}

    for category, cat_data in categories.items():
        cat_keywords = cat_data.get("keywords", [])
        # Include the category name along with its keywords for richer context
        category_context = f"{category}: " + ", ".join(cat_keywords)
        # Use a more instructive prompt format
        prompt = (
            f"Determine the relevance between the following icon tags and the category description.\n\n"
            f"Icon Tags: {icon_description}\n"
            f"Category: {category_context}\n\n"
            f"Provide a relevance score between 0 and 1 (where 1 means a perfect match)."
        )
        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            padding=True
        )
        with torch.no_grad():
            outputs = model(**inputs)
            # Assuming model outputs logits for the score; if a regression head is available, use that
            score = outputs.logits.squeeze().item()
        # Optionally, adjust normalization (for example, divide by token length or keyword count)
        normalized_score = score / (len(cat_keywords) or 1)
        category_scores[category] = normalized_score

        if normalized_score > highest_score:
            highest_score = normalized_score
            best_category = category

    return best_category, highest_score, category_scores



semantic_model_t5_xxl = "sentence-t5-xxl"
semantic_model_mpnet_base_v2 = "all-mpnet-base-v2"


@app.command()
def categorize_icons(
    input_icons: str = typer.Option(..., help="Path to the input JSON file with icon data"),
    output_filtered: str = typer.Option(..., help="Path to save the filtered icons JSON file"),
    output_keywords: str = typer.Option(..., help="Base path for the output translated keyword JSON files"),
    categories: str = typer.Option(..., help="Path to the categories JSON file"),
    categorized_cache: str = typer.Option("data/categorized.json", help="Base path for cached categorized data"),
    limit: int = typer.Option(200, help="Max number of icons to output"),
    languages: str = typer.Option("en,ru", help="Comma-separated list of target languages for translation (e.g. 'fr,de')"),
    translator: str = typer.Option("google", help="Translation service to use (google or openai)"),
    chunk_size: int = typer.Option(90, help="Chunk size for translations"),
    semantic_model_name: str = typer.Option(semantic_model_t5_xxl, help="Name of the semantic embedding model to use")
):
    semantic_model = SentenceTransformer(semantic_model_name)

    def calculate_file_hash(file_path):
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    input_hash = calculate_file_hash(input_icons)
    categorized_cache_path = f"{categorized_cache.rsplit('.', 1)[0]}-{input_hash}.json"

    if os.path.exists(categorized_cache_path):
        typer.echo(f"Loading categorized data from cache: {categorized_cache_path}")
        with open(categorized_cache_path, "r", encoding="utf-8") as f:
            categorized_icons = json.load(f)
    else:
        cat_data = load_categories_from_json(categories)
        icons = load_icons_from_json(input_icons)
        categorized_icons = []
        with typer.progressbar(icons, label="Categorizing icons") as bar:
            for icon in icons:
                tags = icon.get("tags", "")
                enriched_tags = enrich_keywords(tags)
                enriched_tags_str = ", ".join(enriched_tags)
                best_category, highest_score, category_scores = categorize_icon_semantic(
                    enriched_tags_str, cat_data, semantic_model
                )
                icon["best_category"] = best_category
                icon["match_score"] = highest_score
                icon["category_scores"] = category_scores
                # Combine icon keywords with category keywords for robust search
                combined_keywords = set(enriched_tags)
                category_keywords = set(cat_data.get(best_category, {}).get("keywords", []))
                combined_keywords.update(category_keywords)
                icon.setdefault("keywords", {})
                icon["keywords"]["en"] = sorted(combined_keywords)
                icon.setdefault("categories", {})
                icon["categories"][best_category] = cat_data.get(best_category, {})
                categorized_icons.append(icon)
                bar.update(1)

        with open(categorized_cache_path, "w", encoding="utf-8") as f:
            json.dump(categorized_icons, f, ensure_ascii=False, indent=2)
        typer.echo(f"Categorized data saved to cache: {categorized_cache_path}")

    categorized_icons.sort(key=lambda x: x["match_score"], reverse=True)
    grouped_icons = defaultdict(list)
    for icon in categorized_icons:
        grouped_icons[icon["best_category"]].append(icon)

    selected_icons = distribute_icons(grouped_icons, total_limit=limit, min_score=0.0, max_per_category=0)

    combined_keywords = set()
    for icon in selected_icons:
        combined_keywords.update(icon["keywords"]["en"])
    combined_keywords = sorted(combined_keywords)

    lang_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
    for lang in lang_list:
        if lang.lower() == "en":
            continue
        output_file = Path(output_keywords).with_suffix(f".{lang}.json")
        existing_translations = {}
        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                existing_translations = json.load(f)
        untranslated_keywords = set(combined_keywords) - set(existing_translations.keys())
        untranslated_keywords = [word for word in untranslated_keywords if word.isalnum()]
        if not untranslated_keywords:
            typer.echo(f"All keywords already translated for language {lang}. Skipping translation.")
        else:
            typer.echo(f"Translating {len(untranslated_keywords)} keywords to {lang} using {translator}...")
            translation_map = bulk_translate_keywords(
                list(untranslated_keywords),
                target_language=lang,
                translator=translator,
                api_key=openai_api_key,
                chunk_size=chunk_size
            )
            existing_translations.update(translation_map)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(existing_translations, f, ensure_ascii=False, indent=2)
            typer.echo(f"Translated keywords saved to {output_file.as_posix()}")
        for icon in selected_icons:
            icon["keywords"].setdefault(lang, [])
            for kw in icon["keywords"]["en"]:
                if kw in existing_translations:
                    icon["keywords"][lang].append(existing_translations[kw])
            icon["keywords"][lang] = list(set(icon["keywords"][lang]))

    filtered_output = []
    for icon in selected_icons:
        filtered_output.append({
            "style": icon.get("style"),
            "width": icon.get("width"),
            "height": icon.get("height"),
            "score": icon.get("match_score"),
            "tags": icon.get("tags"),
            "name": icon.get("name"),
            "content": icon.get("content"),
            "set_id": icon.get("set_id"),
            "categories": icon.get("categories"),
            "keywords": icon.get("keywords")
        })

    with open(output_filtered, "w", encoding="utf-8") as f:
        json.dump({"icons": filtered_output}, f, ensure_ascii=False, indent=2)

    typer.echo(f"Filtered and categorized icons with translations saved to {output_filtered}")


def translate_with_openai(keywords, target_language, api_key, chunk_size=100):
    translation_map = {}
    keywords = [word for word in keywords if word.isalnum()]
    remaining_keywords = set(keywords)
    max_retries = 100
    max_incomplete_response_retries = 10
    language_name = languages[target_language]
    current_chunk_size = chunk_size
    assert language_name is not None, f"Unsupported language: {target_language}"

    while remaining_keywords:
        chunks = list(chunk_list(list(remaining_keywords), current_chunk_size))
        total_chunks = len(chunks)
        typer.echo(f"Translating {len(remaining_keywords)} keywords in {total_chunks} chunks into {language_name} using OpenAI...")
        incomplete_responses = 0

        for chunk_index, chunk in enumerate(chunks):
            prompt = f"""Please translate the following English keywords into {language_name}:
Return them as a JSON object where keys are the original English words and values are the translations. 
Ensure all words are translated and maintain the order.

Keywords: {json.dumps(chunk)}"""
            chunk_translation = None

            for attempt in range(max_retries):
                try:
                    typer.echo(
                        f"Translating chunk {chunk_index + 1}/{total_chunks} with OpenAI to {language_name}. "
                        f"Attempt {attempt + 1}/{max_retries}: {chunk}"
                    )
                    response = openai_chat(prompt, api_key, model="gpt-4", temperature=0.9)
                    cant_json_decode = False
                    try:
                        chunk_translation = json.loads(response)
                    except json.JSONDecodeError:
                        cant_json_decode = True
                    if not str(response).rstrip(' `\n\r').endswith('}') or cant_json_decode:
                        incomplete_responses += 1
                        if incomplete_responses >= max_incomplete_response_retries:
                            exit(1)
                        else:
                            current_chunk_size = max(1, math.floor(current_chunk_size * 0.95))
                            typer.echo(f"Reducing chunk size due to incomplete response. New chunk size: {current_chunk_size}.")
                            chunk_translation = None
                            raise ValueError(f"Invalid response from OpenAI: {response[:10]}...{response[-10:]}")
                    translation_map.update(chunk_translation)
                    remaining_keywords -= set(chunk_translation.keys())
                    incomplete_responses = 0
                    break
                except Exception as e:
                    typer.echo(f"Error during OpenAI translation: {e}")
                    time.sleep(1)
                if chunk_translation is None:
                    break  # Exit the chunk loop to rebuild chunks with new size

            if chunk_translation is None:
                break  # Exit the chunk loop to rebuild chunks with new size

    return translation_map


def bulk_translate_keywords(keywords, target_language, translator="openai", **kwargs):
    if translator == "openai":
        api_key = kwargs.get("api_key")
        if not api_key:
            raise ValueError("API key is required for OpenAI translation.")
        return translate_with_openai(keywords, target_language, api_key, chunk_size=kwargs.get("chunk_size", 100))
    else:
        raise ValueError(f"Unknown translator: {translator}")


if __name__ == "__main__":
    app()

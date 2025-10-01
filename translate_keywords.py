#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path

import dotenv
import typer
from openai import OpenAI

dotenv.load_dotenv()
app = typer.Typer()

# Constants
MODEL = "gpt-4o"
CONTEXT_WINDOW = 8192  # total tokens: input + output
MAX_TOKENS = 1024  # max tokens for model's output


###############################################################################
# Helper Functions
###############################################################################

def estimate_tokens(text: str) -> int:
    """
    Rough token estimate: ~1 token per 4 characters.
    """
    return len(text) // 4 + 1


def build_prompt(tags_chunk: list, language_label: str) -> str:
    """Builds the translation prompt."""
    return (
        f"Please translate the following English words into {language_label}:\n"
        "Return them as a JSON object where keys are the original words (English) and values are the translations.\n"
        "Words:\n"
        f"{json.dumps(tags_chunk, ensure_ascii=False)}"
    )


def estimate_response_chars(chunk: list, k: float = 2.0) -> int:
    """
    Estimate character count for the JSON response.
    'k' scales the expected length of a translation versus the English word.
    """
    if not chunk:
        return 2  # "{}"
    total_chars = 2  # for '{' and '}'
    for i, tag in enumerate(chunk):
        pair_chars = 5 + len(tag) + int(k * len(tag))
        total_chars += pair_chars
        if i < len(chunk) - 1:
            total_chars += 2  # for comma and space
    return total_chars


import json
import re


def parse_response_safely(response_text: str) -> dict:
    """
    Attempts to extract valid JSON from a potentially truncated or corrupted response.

    1. Finds the substring starting at the first '{' and extends it until braces balance.
       If braces are unbalanced, appends the necessary number of '}'.
    2. Removes any trailing commas just before the closing brace.
    3. If parsing still fails—e.g. because the last property is truncated—it iteratively
       removes the last key-value pair (skipping the corrupted part) until valid JSON is obtained.

    This ensures that the returned JSON object is closed and does not contain a trailing comma.
    If no valid JSON can be extracted, an empty dict is returned.
    """
    # Step 1: Extract candidate substring with balanced braces.
    start = response_text.find('{')
    if start == -1:
        return {}

    count = 0
    end = None
    for i in range(start, len(response_text)):
        if response_text[i] == '{':
            count += 1
        elif response_text[i] == '}':
            count -= 1
            if count == 0:
                end = i
                break
    if end is None:
        # If braces never balance, assume the rest is candidate and append missing '}'.
        candidate = response_text[start:] + ('}' * count)
    else:
        candidate = response_text[start:end + 1]

    # Step 2: Remove trailing commas before the final brace.
    candidate = re.sub(r',\s*}$', '}', candidate)

    # Step 3: Attempt to parse; if it fails, iteratively remove the last property.
    while candidate:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Attempt to remove the last property.
            # This regex finds the last property of the form "key": value (where value can be a string, number, or literal)
            new_candidate = re.sub(
                r',\s*"(?:\\.|[^"\\])*":\s*(?:"(?:\\.|[^"\\])*"|[\d.eE+-]+|true|false|null)\s*}$',
                '}',
                candidate
            )
            if new_candidate == candidate:
                # If regex didn't match, try to find the last comma outside of quotes.
                last_comma = candidate.rfind(',')
                if last_comma == -1:
                    break
                candidate = candidate[:last_comma] + "}"
            else:
                candidate = new_candidate
    return {}


def openai_chat(prompt: str, api_key: str, model: str = MODEL, max_tokens: int = MAX_TOKENS) -> str:
    """
    Calls the OpenAI API with the provided prompt.
    """
    client = OpenAI(api_key=api_key)
    messages = [
        {"role": "system", "content": "You are a skilled translator from English to other languages."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content.strip()


def load_existing_translations(path: Path) -> dict:
    """Loads previously saved translations, if any."""
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_translations(path: Path, data: dict):
    """Writes translations to a JSON file."""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


###############################################################################
# Chunk Calculation
###############################################################################

def fits_context(tags_chunk: list, language_label: str, max_output_tokens: int, total_token_limit: int) -> bool:
    """
    Returns True if this chunk likely fits in the GPT context window.
    """
    prompt_text = build_prompt(tags_chunk, language_label)
    input_tokens = estimate_tokens(prompt_text)
    response_chars = estimate_response_chars(tags_chunk, k=2.0)
    output_tokens = estimate_tokens("x" * response_chars)  # dummy string to estimate tokens
    if output_tokens > max_output_tokens:
        return False
    return (input_tokens + output_tokens) < total_token_limit


def next_chunk_size(tags: list, language_label: str, max_output_tokens: int, total_token_limit: int) -> int:
    """
    Determines the maximum number of items from 'tags' that can be sent without exceeding the context.
    """
    chunk = []
    for tag in tags:
        test_chunk = chunk + [tag]
        if not fits_context(test_chunk, language_label, max_output_tokens, total_token_limit):
            break
        chunk = test_chunk
    return len(chunk)


###############################################################################
# Translation Logic
###############################################################################

def translate_chunk_retry(chunk: list, language_label: str, api_key: str, max_attempts: int = 3) -> dict:
    """
    Translates a chunk with retry logic.
    Returns a parsed dictionary (even if partial).
    """
    prompt = build_prompt(chunk, language_label)
    for attempt in range(1, max_attempts + 1):
        response = None
        try:
            response = None
            response = openai_chat(prompt, api_key=api_key)
            typer.echo(f"\nReceived response: {response}")
            result = parse_response_safely(response)
            if result:
                return result
        except Exception as e:
            typer.echo(f"Chunk translation attempt {attempt} failed: {e}")
        time.sleep(1)
    return {}


###############################################################################
# Main Command
###############################################################################

@app.command()
def translate_keywords(
        source_file: str = typer.Option("data/icons.stripped.en.json", help="Path to source JSON"),
        languages: str = typer.Option(
            ...,
            help="Comma-separated list of languages (e.g., 'ru,fr'). Example: --languages ru,fr",
            show_default=False
        ),
        openai_api_key: str = typer.Option(None, help="OpenAI API key")
):
    """
    Translates tags from the source file into specified languages.
    Usage example:
        python3 translate_keywords.py --languages ru,en,fr
    Dynamically adjusts the chunk size so as not to exceed GPT's context limit.
    Updates the target translation file with successful translations.
    """
    # Validate API key.
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        typer.echo("Error: OPENAI_API_KEY is missing")
        raise typer.Exit(code=1)

    # Load source data.
    src_path = Path(source_file)
    if not src_path.exists():
        typer.echo(f"Error: Source file not found: {src_path}")
        raise typer.Exit(code=1)
    with src_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    icons = data.get("icons", [])
    all_tags = sorted(set(
        tag.strip()
        for icon in icons
        for tag in icon.get("tags", "").split(",")
        if tag.strip()
    ))
    typer.echo(f"Found {len(all_tags)} unique tags total in {source_file}.")

    # Process each language.
    lang_list = [lang.strip() for lang in languages.split(",") if lang.strip()]
    for lang_code in lang_list:
        language_label = f"{lang_code} language"
        out_file = Path("data") / f"keywords.{lang_code}.json"
        existing_map = load_existing_translations(out_file)

        # Build list of tags that still need translation.
        to_translate = [t for t in all_tags if t not in existing_map]
        if not to_translate:
            typer.echo(f"All tags translated for '{lang_code}'. Skipping.")
            continue

        total_left = len(to_translate)
        typer.echo(f"\nTranslating {total_left} tags into '{lang_code}' => {out_file}")
        with typer.progressbar(length=total_left, label=f"Translating => {lang_code}") as pbar:
            # Initialize current_chunk_size based on the remaining list.
            current_chunk_size = next_chunk_size(to_translate, language_label, MAX_TOKENS, CONTEXT_WINDOW)
            if current_chunk_size == 0:
                current_chunk_size = 1

            while to_translate:
                if current_chunk_size > len(to_translate):
                    current_chunk_size = len(to_translate)
                chunk = to_translate[:current_chunk_size]
                typer.echo(f"\nTranslating chunk of {len(chunk)} keywords")
                partial_map = translate_chunk_retry(chunk, language_label, api_key)

                if partial_map:
                    # Update target dictionary with translations.
                    for k, v in partial_map.items():
                        existing_map[k] = v
                    save_translations(out_file, existing_map)

                    # Determine which items in the chunk were translated.
                    translated = [item for item in chunk if item in partial_map]
                    pbar.update(len(translated))
                    typer.echo(f"Translated {len(translated)} keywords from chunk.")

                    # Remove translated items from the list.
                    # (Keep items not translated at the front.)
                    to_translate = [item for item in chunk if item not in partial_map] + to_translate[
                                                                                         current_chunk_size:]

                    if len(translated) < len(chunk):
                        # Partial success: shrink chunk size.
                        current_chunk_size = max(1, current_chunk_size // 2)
                        typer.echo(f"Partial success. Reduced chunk size to {current_chunk_size}.")
                    else:
                        # Full success: try increasing chunk size slightly.
                        recalculated = next_chunk_size(to_translate, language_label, MAX_TOKENS, CONTEXT_WINDOW)
                        current_chunk_size = max(1, int((current_chunk_size + recalculated) / 2))
                        typer.echo(f"Full success. Adjusted chunk size to {current_chunk_size}.")
                else:
                    # No translation obtained.
                    if current_chunk_size == 1:
                        typer.echo(f"Skipping item '{chunk[0]}' due to repeated failures.")
                        pbar.update(1)
                        to_translate = to_translate[1:]
                    else:
                        current_chunk_size = max(1, current_chunk_size // 2)
                        typer.echo(f"No success. Reduced chunk size to {current_chunk_size}.")

        typer.echo(f"Finished translating '{lang_code}' => {out_file}")


if __name__ == "__main__":
    app()

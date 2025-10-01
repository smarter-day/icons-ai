"""Translation-specific helper functions."""

import json
import time
from pathlib import Path
from typing import Any

import typer
from openai import OpenAI

from library.ai import build_prompt, parse_response_safely


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


def openai_chat(prompt: str, api_key: str, model: str, max_tokens: int) -> str:
    """
    Calls the OpenAI API with the provided prompt.
    """
    client = OpenAI(api_key=api_key)
    messages: list[Any] = [
        {"role": "system", "content": "You are a skilled translator "
                 "from English to other languages."},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens
    )
    return str(response.choices[0].message.content).strip()


def translate_chunk_retry(chunk: list, language_label: str, api_key: str,
                          model: str, max_tokens: int,
                          max_attempts: int = 3) -> dict:
    """
    Translates a chunk with retry logic.
    Returns a parsed dictionary (even if partial).
    """
    prompt = build_prompt(chunk, language_label)
    for attempt in range(1, max_attempts + 1):
        response = None
        try:
            response = None
            response = openai_chat(prompt, api_key=api_key, model=model,
                                   max_tokens=max_tokens)
            typer.echo(f"\nReceived response: {response}")
            result = parse_response_safely(response)
            if result:
                return result
        except Exception as e:
            typer.echo(f"Chunk translation attempt {attempt} failed: {e}")
        time.sleep(1)
    if chunk:
        typer.echo(
            "⚠️ Failed to parse any translations for last chunk; "
            "will retry remaining tags only."
        )
    return {}

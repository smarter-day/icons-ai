"""AI-related helper functions for translation and language processing."""

import json
import re


def estimate_tokens(text: str) -> int:
    """
    Rough token estimate: ~1 token per 4 characters.
    """
    return len(text) // 4 + 1


def build_prompt(tags_chunk: list, language_label: str) -> str:
    """Builds the translation prompt."""
    return (
        "Please translate the following English "
        f"words into {language_label}:\n"
        "Return them as a JSON object where keys are the original words "
        "(English) and values are the translations.\n"
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


def parse_response_safely(response_text: str) -> dict:
    """
    Attempts to extract valid JSON from a potentially truncated or
    corrupted response.

    1. Finds the substring starting at the first '{'
       and extends it until braces balance.
       If braces are unbalanced, appends the necessary number of '}'.
    2. Removes any trailing commas just before the closing brace.
    3. If parsing still fails—e.g. because the last property
       is truncated—it iteratively
       removes the last key-value pair (skipping the corrupted part)
       until valid JSON is obtained.

    This ensures that the returned JSON object is closed
    and does not contain a trailing comma.
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
    truncated_input = False
    if end is None:
        truncated_input = True
        # If braces never balance, assume the rest
        # is candidate and append missing '}'.
        candidate = response_text[start:] + ('}' * count)
    else:
        candidate = response_text[start:end + 1]

    # Step 2: Remove trailing commas before the final brace.
    candidate = re.sub(r',\s*}$', '}', candidate)

    # Step 3: Attempt to parse; if it fails,
    # iteratively remove the last property.
    had_to_trim = False
    while candidate:
        try:
            result = json.loads(candidate)
            if truncated_input or had_to_trim:
                print(
                    f"✓ Parsed {len(result)} translations "
                    "after recovering truncated response"
                )
            return result
        except json.JSONDecodeError:
            had_to_trim = True
            # Attempt to remove the last property.
            # This regex finds the last property of the form "key": value
            # (where value can be a string, number, or literal)
            new_candidate = re.sub(
                r',\s*"(?:\\.|[^"\\])*":\s*(?:"(?:\\.|[^"\\])*"|[\d.eE+-]+|true|false|null)\s*}$',
                '}',
                candidate
            )
            if new_candidate == candidate:
                # If regex didn't match, try to find
                # the last comma outside of quotes.
                last_comma = candidate.rfind(',')
                if last_comma == -1:
                    break
                candidate = candidate[:last_comma] + "}"
            else:
                candidate = new_candidate

    # Step 4: If all else fails, try to extract complete key-value
    # pairs from partial response
    # Look for complete pairs that end with comma and quote
    partial_matches = re.findall(r'"([^"]+)":\s*"([^"]+)"\s*,', response_text)
    if partial_matches:
        print(f"✓ Recovered {len(partial_matches)} "
              "partial translations from truncated response")
        return dict(partial_matches)
    return {}


def fits_context(tags_chunk: list, language_label: str,
                 max_output_tokens: int, total_token_limit: int) -> bool:
    """
    Returns True if this chunk likely fits in the GPT context window.
    """
    prompt_text = build_prompt(tags_chunk, language_label)
    input_tokens = estimate_tokens(prompt_text)
    response_chars = estimate_response_chars(tags_chunk, k=2.0)
    output_tokens = estimate_tokens("x" * response_chars)
    if output_tokens > max_output_tokens:
        return False
    return (input_tokens + output_tokens) < total_token_limit

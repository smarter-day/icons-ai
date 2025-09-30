#!/usr/bin/env python

import os
import json
import math
import sys

LANGUAGE = sys.argv[1]

assert LANGUAGE, "Please provide a language code"

if LANGUAGE == "en":
    ICON_EMBEDDINGS_JSON = f"embeddings/icon_embeddings.json"
    WORD_EMBEDDINGS_JSON = f"embeddings/vocab_embeddings.json"
else:
    ICON_EMBEDDINGS_JSON = f"embeddings/icon_embeddings.{LANGUAGE}.json"
    WORD_EMBEDDINGS_JSON = f"embeddings/vocab_embeddings.{LANGUAGE}.json"

def load_json_embeddings():
    if not os.path.exists(ICON_EMBEDDINGS_JSON):
        raise FileNotFoundError(f"Missing {ICON_EMBEDDINGS_JSON}")
    if not os.path.exists(WORD_EMBEDDINGS_JSON):
        raise FileNotFoundError(f"Missing {WORD_EMBEDDINGS_JSON}")

    with open(ICON_EMBEDDINGS_JSON, "r", encoding="utf-8") as f:
        icon_embeds = json.load(f)
    with open(WORD_EMBEDDINGS_JSON, "r", encoding="utf-8") as f:
        vocab_embeds = json.load(f)

    return icon_embeds, vocab_embeds


def average_embedding(text: str, vocab: dict, similarity_threshold: float = 0.7):
    """
    - Tokenize text
    - For each token, find exact or fuzzy match in vocab
    - Average the embeddings
    - Return list of floats
    """
    tokens = text.lower().replace(",", " ").split()
    vecs = []

    for t in tokens:
        if t in vocab:
            # Exact match
            vecs.append(vocab[t])
        else:
            # Fuzzy match - find closest word in vocabulary
            close_matches = get_close_matches(t, vocab.keys(), n=1, cutoff=similarity_threshold)
            if close_matches:
                closest_word = close_matches[0]
                vecs.append(vocab[closest_word])
                print(f"Using '{closest_word}' for '{t}'")  # Optional: log the correction

    if not vecs:
        # If still no matches, try character-level similarity for the whole query
        close_matches = get_close_matches(text.lower(), vocab.keys(), n=1, cutoff=0.5)
        if close_matches:
            vecs.append(vocab[close_matches[0]])
        else:
            return None  # or a zero vector

    # average
    dim = len(vecs[0])
    sums = [0.0] * dim
    for v in vecs:
        for i in range(dim):
            sums[i] += v[i]
    count = len(vecs)
    return [val / count for val in sums]


def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    This is the minimum number of single-character edits required.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Cost of insertions, deletions, or substitutions
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def get_close_matches(word, possibilities, n=3, cutoff=0.6):
    """
    Find close matches to 'word' in list of 'possibilities'.

    Args:
        word: Target string to match
        possibilities: List of possible strings to match against
        n: Maximum number of close matches to return
        cutoff: Similarity threshold (0.0 to 1.0)

    Returns:
        List of the best n matches that meet the cutoff
    """
    if not word or not possibilities:
        return []

    word_lower = word.lower()
    matches = []

    for possibility in possibilities:
        # Calculate similarity score (1 - normalized distance)
        distance = levenshtein_distance(word_lower, possibility.lower())
        max_len = max(len(word), len(possibility))
        if max_len == 0:
            similarity = 1.0
        else:
            similarity = 1.0 - (distance / max_len)

        if similarity >= cutoff:
            matches.append((possibility, similarity))

    # Sort by similarity (highest first) and return top n
    matches.sort(key=lambda x: x[1], reverse=True)
    return [match[0] for match in matches[:n]]


def cosine_similarity(v1, v2):
    """
    v1, v2 are lists of floats
    """
    if len(v1) != len(v2):
        return 0.0
    dot = 0.0
    norm1 = 0.0
    norm2 = 0.0
    for a, b in zip(v1, v2):
        dot += a*b
        norm1 += a*a
        norm2 += b*b
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (math.sqrt(norm1)*math.sqrt(norm2))

def search_icons(query, top_k=5):
    """
    1) Embed query from words
    2) Compare to icon embeddings by cos sim
    3) Return top_k
    """
    icon_embeds, vocab_embeds = load_json_embeddings()
    query_vec = average_embedding(query, vocab_embeds)
    if query_vec is None:
        return []  # no known words in query

    # Compare
    results = []
    for icon_id, icon_vec in icon_embeds.items():
        sim = cosine_similarity(query_vec, icon_vec)
        results.append((icon_id, sim))

    # Sort desc by similarity
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]

def main():
    while True:
        user_input = input("\nEnter search query (or blank to quit): ")
        user_input = user_input.strip()
        if not user_input:
            break
        top_results = search_icons(user_input, top_k=20)
        for icon_id, sim in top_results:
            print(f"[{sim:.3f}]  {icon_id}")

if __name__ == "__main__":
    main()

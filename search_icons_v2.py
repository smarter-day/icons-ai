#!/usr/bin/env python

import json
import os
import re
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import typer

from library.project import Project
from library.settings import ProjectSettings

app = typer.Typer(
    help="Interactive icon search against precomputed embeddings"
)

# Stopwords (unchanged for compatibility)
STOPWORDS: Dict[str, set[str]] = {
    "en": {
        "a", "an", "and", "are", "as", "at", "be", "been", "being", "but", "by",
        "can", "could", "did", "do", "does", "for", "from", "had", "has", "have",
        "he", "her", "him", "his", "i", "if", "in", "is", "it", "its", "me", "my",
        "not", "of", "on", "or", "our", "she", "that", "the", "their", "there",
        "they", "this", "to", "was", "we", "were", "what", "when", "where", "which",
        "who", "will", "with", "would", "you", "your",
    },
    "ru": {
        "а", "без", "бери", "бы", "был", "была", "были", "было", "в", "во",
        "вот", "все", "всего", "всех", "вы", "где", "да", "для", "до", "его",
        "ее", "ей", "ему", "если", "есть", "ещё", "же", "за", "и", "из", "или",
        "к", "как", "когда", "кто", "ли", "на", "над", "не", "нет", "ни", "о",
        "об", "от", "по", "под", "при", "с", "со", "так", "то", "того", "тоже",
        "ты", "у", "чего", "что", "это", "этом",
    },
    "fr": {
        "à", "au", "aux", "avec", "ce", "ces", "cette", "d'", "dans", "de", "des",
        "du", "elle", "en", "es", "est", "et", "eux", "il", "ils", "je", "la",
        "le", "les", "leur", "lui", "ma", "mais", "me", "mon", "ne", "nos", "notre",
        "on", "ou", "par", "pas", "pour", "qu'", "que", "qui", "sa", "se", "ses",
        "son", "sont", "sur", "ta", "te", "toi", "ton", "tu", "un", "une", "vous",
    },
    "es": {
        "a", "al", "con", "como", "de", "del", "desde", "el", "ella", "en", "es",
        "esa", "ese", "eso", "esta", "este", "esto", "hasta", "la", "las", "lo",
        "los", "me", "mi", "mis", "no", "nos", "o", "para", "por", "que", "se",
        "sin", "su", "sus", "te", "tu", "un", "una", "y", "yo",
    },
    "de": {
        "als", "am", "an", "auf", "aus", "bei", "bin", "bist", "das", "dem", "den",
        "der", "des", "die", "ein", "eine", "einem", "einen", "einer", "es", "für",
        "hat", "habe", "haben", "im", "in", "ist", "mit", "nach", "nicht", "oder",
        "sein", "sie", "sind", "über", "und", "uns", "vom", "von", "was", "wer",
        "wie", "wir", "zu", "zum", "zur",
    },
    "it": {
        "a", "al", "che", "come", "con", "da", "dal", "dall'", "dalla", "de", "del",
        "dell'", "della", "di", "e", "gli", "i", "il", "in", "l'", "la", "le", "lo",
        "ma", "mi", "non", "o", "per", "s'", "se", "si", "sono", "su", "sul",
        "sull'", "sulla", "ti", "un", "una", "uno",
    },
    "pt": {
        "a", "as", "com", "da", "das", "de", "do", "dos", "e", "ela", "ele", "em",
        "es", "esta", "este", "eu", "foi", "mas", "me", "meu", "minha", "na", "nas",
        "no", "nos", "o", "os", "ou", "para", "por", "que", "são", "se", "sem",
        "seu", "sua", "tu", "um", "uma", "você",
    },
    "zh": {
        "的", "了", "和", "及", "与", "在", "是", "有", "也", "不", "为", "于",
        "就", "而", "被", "从", "到", "这", "那", "他", "她", "它", "我", "你",
        "们", "之", "以", "会", "可", "很", "都", "没", "个", "时", "对",
        "上", "下", "里", "来", "去",
    },
}

# Simplified prefixes/suffixes to reduce over-normalization
PREFIXES_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "en": (
        "anti", "auto", "bi", "co", "counter", "de", "dis", "en", "ex", "fore",
        "hyper", "in", "inter", "mid", "mis", "non", "over", "pre", "pro", "re",
        "semi", "sub", "super", "trans", "un", "under",
    ),
    "es": (
        "a", "ante", "anti", "bajo", "con", "contra", "de", "des", "en", "entre",
        "ex", "extra", "in", "inter", "para", "pre", "pro", "re", "sin", "sobre",
        "sub", "super", "trans",
    ),
    "fr": (
        "anti", "auto", "co", "contre", "dé", "dés", "en", "entre", "ex", "hyper",
        "in", "inter", "para", "pré", "pro", "re", "sans", "sous", "super", "sur",
        "trans",
    ),
    "de": (
        "ab", "an", "auf", "aus", "be", "ent", "er", "ge", "her", "hin",
        "hinter", "miss", "mit", "nach", "nieder", "über", "um", "unter", "ver",
        "vor", "zer",
    ),
    "it": (
        "a", "anti", "auto", "co", "contro", "de", "dis", "extra", "in", "inter",
        "per", "pre", "pro", "ri", "s", "semi", "sotto", "sovra", "stra", "su",
        "trans",
    ),
    "pt": (
        "a", "ante", "anti", "co", "com", "contra", "de", "des", "em", "entre",
        "ex", "in", "inter", "para", "pre", "pro", "re", "sem", "sobre", "sub",
        "super", "trans",
    ),
    "ru": (
        "без", "в", "вз", "во", "вы", "до", "за", "из", "на", "над", "не",
        "недо", "об", "от", "пере", "по", "под", "пре", "при", "про", "раз",
        "с", "со", "у",
    ),
}

SUFFIXES_DROP_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "en": (
        "able", "al", "ance", "ation", "ed", "ence", "er", "es", "est", "ful",
        "ic", "ing", "ion", "ism", "ist", "ity", "ive", "less", "ly", "ment",
        "ness", "or", "s", "ship", "tion",
    ),
    "es": (
        "ación", "ado", "al", "amiento", "anza", "ción", "dor", "es", "ez",
        "idad", "ido", "ión", "ismo", "ista", "mente", "or", "s", "sión", "ura",
    ),
    "fr": (
        "age", "ance", "ant", "ation", "é", "ée", "ement", "ence", "ent", "eur",
        "euse", "ion", "ique", "isme", "iste", "ment", "s", "tion",
    ),
    "de": (
        "chen", "e", "en", "er", "heit", "ig", "in", "ion", "ismus", "ist",
        "keit", "lich", "ling", "schaft", "ung",
    ),
    "it": (
        "ale", "ante", "anza", "are", "azione", "enza", "ere", "ice", "ile",
        "ino", "ismo", "ista", "ità", "mento", "o", "one", "ore", "re", "sione",
        "ta", "to", "ti", "zione",
    ),
    "pt": (
        "ação", "ado", "agem", "al", "amento", "ança", "ção", "dade", "dor",
        "eira", "eiro", "es", "ismo", "ista", "mento", "or", "s", "são", "ura",
    ),
    "ru": (
        "а", "ая", "е", "ее", "ей", "ем", "ему", "и", "ие", "ий", "им", "ими",
        "их", "ия", "о", "ов", "ого", "ое", "ой", "ом", "ому", "у", "ы", "ый",
        "я", "ям", "ями", "ях",
    ),
}

REFLEXIVE_SUFFIXES_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "en": (),
    "es": ("se",),
    "fr": ("se", "s'", "me", "m'", "te", "t'"),
    "de": ("sich",),
    "it": ("si", "mi", "ti", "ci", "vi"),
    "pt": ("se", "me", "te"),
    "ru": ("ся", "сь"),
    "zh": (),
}


def get_stopwords(language: str) -> set[str]:
    language = (language or "").split("-")[0].lower()
    return STOPWORDS.get(language, set())


def tokenize(text: str, stopwords: set[str]) -> List[str]:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return [token for token in tokens if token and token not in stopwords]


def normalize_token_variants(token: str, language: str | None) -> List[str]:
    """Generate normalized variants with stricter rules to preserve intent."""
    variants = [token.lower()]
    lang = (language or "").split("-")[0].lower()
    prefixes = PREFIXES_BY_LANG.get(lang, ())
    suffixes = SUFFIXES_DROP_BY_LANG.get(lang, ())
    reflexive_suffixes = REFLEXIVE_SUFFIXES_BY_LANG.get(lang, ())

    # Only normalize if token is long enough to avoid overgeneralization
    if len(token) >= 4:
        for suffix in reflexive_suffixes:
            if token.endswith(suffix):
                variants.append(token[:-len(suffix)])
        for prefix in prefixes:
            if token.startswith(prefix) and len(token) - len(prefix) >= 3:
                variants.append(token[len(prefix):])
        for suffix in suffixes:
            if token.endswith(suffix) and len(token) - len(suffix) >= 3:
                variants.append(token[:-len(suffix)])

    return list(set(variants))


def load_json_embeddings(
    language: str,
) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
    base_dir = os.getcwd()
    icon_path = os.path.join(base_dir, "embeddings", f"icon_embeddings.{language}.json")
    vocab_path = os.path.join(base_dir, "embeddings", f"vocab_embeddings.{language}.json")

    if not os.path.exists(icon_path):
        raise FileNotFoundError(f"Missing {icon_path}")
    if not os.path.exists(vocab_path):
        raise FileNotFoundError(f"Missing {vocab_path}")

    with open(icon_path, "r", encoding="utf-8") as f:
        icon_embeds = json.load(f)
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab_embeds = json.load(f)

    return icon_embeds, vocab_embeds


def dot_product(v1: Sequence[float], v2: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))


def vector_norm(vec: Sequence[float]) -> float:
    return dot_product(vec, vec) ** 0.5


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if len(s2) == 0:
        return len(s1)
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def get_close_matches(
    word: str,
    possibilities: Iterable[str],
    n: int = 1,
    cutoff: float = 0.85,
    query_length: int = 1,
) -> List[Tuple[str, float]]:
    """Context-aware fuzzy matching with dynamic cutoff."""
    if not word:
        return []

    word_lower = word.lower()
    scored_matches = []
    # Adjust cutoff based on query complexity (longer queries allow looser matches)
    dynamic_cutoff = max(cutoff, 0.9 - 0.05 * query_length)

    for possibility in possibilities:
        candidate_lower = possibility.lower()
        distance = levenshtein_distance(word_lower, candidate_lower)
        max_len = max(len(word_lower), len(candidate_lower))
        similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0

        # Boost score for longer tokens or exact prefix matches
        if len(word_lower) >= 4 and candidate_lower.startswith(word_lower[:3]):
            similarity += 0.1
        # Penalize if lengths differ significantly
        if abs(len(word_lower) - len(candidate_lower)) > 3:
            similarity -= 0.1

        similarity = min(1.0, similarity)  # Cap at 1.0

        if similarity >= dynamic_cutoff:
            scored_matches.append((possibility, similarity))

    scored_matches.sort(key=lambda item: item[1], reverse=True)
    return scored_matches[:n]


def compute_token_weights(tokens: List[str], stopwords: set[str]) -> List[float]:
    """Assign weights to tokens based on length and stopword status."""
    weights = []
    for token in tokens:
        weight = len(token) / 5.0  # Longer tokens are more significant
        if token not in stopwords:
            weight *= 1.5  # Boost non-stopwords
        weights.append(max(0.5, min(weight, 2.0)))  # Clamp between 0.5 and 2.0
    return weights


def search_icons(
    query: str,
    icon_index: Sequence[Tuple[str, List[float], float]],
    vocab_embeds: Dict[str, List[float]],
    stopwords: set[str],
    language: str,
    top_k: int = 20,
    sensitivity: float = 0.85,
) -> List[Tuple[str, float]]:
    """Sophisticated search with weighted token embeddings and token overlap."""
    tokens = tokenize(query, stopwords)
    if not tokens:
        return []

    # Compute token weights
    token_weights = compute_token_weights(tokens, stopwords)

    # Collect embeddings for tokens and their variants
    weighted_vectors: List[Tuple[List[float], float, str]] = []
    matched_tokens = []
    for token, weight in zip(tokens, token_weights):
        found = False
        for variant in normalize_token_variants(token, language):
            if variant in vocab_embeds:
                weighted_vectors.append((vocab_embeds[variant], weight, variant))
                matched_tokens.append(variant)
                found = True
                break
        if not found:
            # Try fuzzy on each variant
            for variant in normalize_token_variants(token, language):
                close_matches = get_close_matches(
                    variant,
                    vocab_embeds.keys(),
                    n=1,
                    cutoff=sensitivity,
                    query_length=len(tokens),
                )
                if close_matches:
                    best_word, score = close_matches[0]
                    typer.echo(f"Using fuzzy match '{best_word}' (score: {score:.3f}) for '{token}' via variant '{variant}'")
                    weighted_vectors.append((vocab_embeds[best_word], weight * score, best_word))
                    matched_tokens.append(best_word)
                    found = True
                    break

    if not weighted_vectors:
        # Try full query as a last resort
        close_matches = get_close_matches(
            query.lower(),
            vocab_embeds.keys(),
            n=1,
            cutoff=sensitivity,
            query_length=1,
        )
        if close_matches:
            best_word, score = close_matches[0]
            weighted_vectors.append((vocab_embeds[best_word], score, best_word))
            matched_tokens.append(best_word)

    if not weighted_vectors:
        return []

    # Weighted average of embeddings
    dim = len(weighted_vectors[0][0])
    query_vec = [0.0] * dim
    total_weight = 0.0
    for vec, weight, _ in weighted_vectors:
        for i, value in enumerate(vec):
            query_vec[i] += weight * value
        total_weight += weight

    if total_weight == 0.0:
        return []

    query_vec = [v / total_weight for v in query_vec]
    query_norm = vector_norm(query_vec)
    if query_norm == 0.0:
        return []

    # Compute token overlap for each icon (using icon_id or description if available)
    icon_token_cache = {}  # Cache for icon tokens (assumes icon_id reflects description)

    def get_icon_tokens(icon_id: str) -> List[str]:
        if icon_id not in icon_token_cache:
            # Approximate tokens from icon_id (replace with description if available)
            icon_token_cache[icon_id] = tokenize(icon_id.replace("_", " "), stopwords)
        return icon_token_cache[icon_id]

    # Rank icons with combined cosine similarity and token overlap
    scored = []
    for icon_id, icon_vec, icon_norm in icon_index:
        cosine_sim = dot_product(query_vec, icon_vec) / (query_norm * icon_norm)

        # Compute token overlap score
        query_tokens = set(matched_tokens)
        icon_tokens = set(get_icon_tokens(icon_id))
        overlap = len(query_tokens & icon_tokens) / max(len(query_tokens), 1)
        overlap_boost = 0.3 * overlap  # Weight overlap contribution

        # Combine scores (adjust weights as needed)
        final_score = 0.7 * cosine_sim + 0.3 * overlap_boost
        scored.append((icon_id, final_score))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


def build_icon_index(
    icon_embeds: Dict[str, List[float]]
) -> List[Tuple[str, List[float], float]]:
    index = []
    for icon_id, vector in icon_embeds.items():
        norm = vector_norm(vector)
        if norm == 0.0:
            continue
        index.append((icon_id, vector, norm))
    return index


@app.command()
def main(
    language: str = typer.Argument(..., help="Language code, e.g. 'ru'"),
    project_file: str = typer.Option(
        None,
        "--project",
        help="Path to the project YAML config file (defaults to DEFAULT_PROJECT)",
    ),
    top_k: int = typer.Option(
        10,
        "--top-k",
        help="Number of results to display for each query",
    ),
    sensitivity: float = typer.Option(
        0.85,
        "--sensitivity",
        help="Sensitivity for fuzzy token matching (0.0-1.0, higher = stricter)",
    ),
) -> None:
    project = Project(project_file)
    _ = project.Settings(ProjectSettings)

    icon_embeds, vocab_embeds = load_json_embeddings(language)
    if not icon_embeds:
        raise ValueError("Icon embeddings are empty – run create_icons_embeddings.py first")

    icon_index = build_icon_index(icon_embeds)
    if not icon_index:
        raise ValueError("No icon vectors with non-zero norm were found")

    stopwords = get_stopwords(language)

    while True:
        try:
            user_input = input("\nEnter search query (or blank to quit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            break

        results = search_icons(
            user_input,
            icon_index,
            vocab_embeds,
            stopwords,
            language,
            top_k=top_k,
            sensitivity=sensitivity,
        )

        if not results:
            typer.echo("No results found.")
            continue

        for icon_id, score in results:
            typer.echo(f"[{score:.3f}]  {icon_id}")


if __name__ == "__main__":
    app()

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
# Language → stopword set. Lists are intentionally modest: they cover the most
# frequent function words in each language, yet stay short enough to maintain
# readability and make porting to Swift straightforward.
STOPWORDS: Dict[str, set[str]] = {
    "en": {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for",
        "from", "has", "he", "in", "is", "it", "its", "of", "on", "or",
        "she", "that", "the", "to", "was", "were", "will", "with",
    },
    "ru": {
        "и", "в", "во", "на", "по", "со", "от", "к", "до", "для", "как",
        "что", "или", "но", "же", "ли", "это", "то", "так", "бы", "не",
        "из", "а", "у", "ну",
    },
    "fr": {
        "le", "la", "les", "un", "une", "et", "ou", "de", "des", "du",
        "en", "dans", "pour", "par", "que", "qui", "sur", "avec", "au",
        "aux", "se", "est", "sont", "pas",
    },
    "es": {
        "el", "la", "los", "las", "un", "una", "y", "o", "de", "del",
        "en", "por", "para", "que", "con", "al", "como", "es", "son",
        "no", "se", "su",
    },
    "de": {
        "der", "die", "das", "ein", "eine", "und", "oder", "zu", "in",
        "im", "vom", "mit", "auf", "für", "als", "ist", "sind", "den",
        "des", "dem", "nicht",
    },
    "it": {
        "il", "lo", "la", "i", "gli", "le", "un", "una", "e", "o",
        "di", "del", "della", "in", "su", "per", "con", "che", "come",
        "sono", "non",
    },
    "pt": {
        "o", "a", "os", "as", "um", "uma", "e", "ou", "de", "do",
        "da", "dos", "das", "em", "no", "na", "nos", "nas", "que",
        "com", "para", "por", "se",
    },
    "zh": {
        "的", "了", "和", "及", "与", "在", "是", "有", "也", "不", "为", "于", "就",
        "而", "被", "从",
    },
}


PREFIXES_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "en": (
        "anti",
        "auto",
        "de",
        "dis",
        "en",
        "em",
        "in",
        "im",
        "inter",
        "mis",
        "non",
        "over",
        "pre",
        "re",
        "sub",
        "trans",
        "un",
    ),
    "es": (
        "des",
        "in",
        "im",
        "pre",
        "re",
        "sobre",
        "sub",
    ),
    "fr": (
        "anti",
        "dé",
        "dés",
        "in",
        "im",
        "inter",
        "mal",
        "pré",
        "re",
        "sur",
        "trans",
    ),
    "de": (
        "be",
        "ent",
        "er",
        "ge",
        "miss",
        "nach",
        "über",
        "unter",
        "ver",
        "zer",
    ),
    "it": (
        "anti",
        "dis",
        "in",
        "im",
        "pre",
        "ri",
        "sovra",
        "sotto",
    ),
    "pt": (
        "anti",
        "des",
        "in",
        "im",
        "pre",
        "re",
        "sobre",
        "sub",
    ),
    "ru": (
        "пере",
        "перео",
        "переоб",
        "под",
        "над",
        "об",
        "от",
        "за",
        "по",
        "про",
        "при",
        "раз",
        "пред",
        "на",
    ),
}


SUFFIXES_DROP_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "en": (
        "ing",
        "ed",
        "er",
        "est",
        "ly",
        "ness",
        "ment",
        "ful",
        "less",
        "s",
        "es",
    ),
    "es": (
        "mente",
        "ción",
        "sión",
        "ando",
        "endo",
        "ado",
        "ido",
        "es",
        "s",
        "mente",
        "mente",
        "mente",
        "mente",
        "mente",
        "mente",
        "mente",
    ),
    "fr": (
        "ement",
        "ement",
        "tion",
        "sion",
        "ment",
        "ant",
        "ent",
        "eur",
        "euse",
        "es",
        "s",
    ),
    "de": (
        "lich",
        "keit",
        "heit",
        "ung",
        "schaft",
        "isch",
        "ig",
        "en",
        "er",
        "e",
        "s",
    ),
    "it": (
        "mente",
        "zione",
        "sione",
        "tà",
        "tà",
        "zione",
        "sione",
        "re",
        "to",
        "ti",
        "re",
        "te",
    ),
    "pt": (
        "mente",
        "ção",
        "são",
        "dade",
        "mente",
        "eiro",
        "eira",
        "es",
        "s",
    ),
    "ru": (
        "ками",
        "ами",
        "ями",
        "ев",
        "ов",
        "емой",
        "ому",
        "ему",
        "ого",
        "его",
        "ыми",
        "ими",
        "ий",
        "ый",
        "ой",
        "ей",
        "ая",
        "яя",
        "ое",
        "ее",
        "ие",
        "ые",
        "ом",
        "ем",
        "ам",
        "ям",
        "ах",
        "ях",
        "ою",
        "ею",
        "ую",
        "ю",
        "а",
        "я",
        "у",
        "ы",
        "и",
        "е",
        "о",
    ),
}


REFLEXIVE_SUFFIXES_BY_LANG: Dict[str, Tuple[str, ...]] = {
    "ru": ("ся", "сь"),
}


def get_stopwords(language: str) -> set[str]:
    language = (language or "").split("-")[0].lower()
    return STOPWORDS.get(language, set())


def tokenize(text: str, stopwords: set[str]) -> List[str]:
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return [token for token in tokens if token and token not in stopwords]


def normalize_token_variants(token: str, language: str | None) -> List[str]:
    """Return candidate normalised variants for a token based on language heuristics."""

    variants: List[str] = []
    seen: set[str] = set()

    def add_variant(value: str) -> None:
        if value and value not in seen:
            variants.append(value)
            seen.add(value)

    lower = token.lower()
    add_variant(lower)
    if "ё" in lower:
        add_variant(lower.replace("ё", "е"))

    lang = (language or "").split("-")[0].lower()
    prefixes = PREFIXES_BY_LANG.get(lang, ())
    suffixes = SUFFIXES_DROP_BY_LANG.get(lang, ())
    reflexive_suffixes = REFLEXIVE_SUFFIXES_BY_LANG.get(lang, ())

    if not prefixes and not suffixes and not reflexive_suffixes:
        return variants

    queue: List[str] = list(variants)

    while queue:
        current = queue.pop(0)

        for suffix in reflexive_suffixes:
            if current.endswith(suffix) and len(current) - len(suffix) >= 3:
                candidate = current[: -len(suffix)]
                if candidate not in seen:
                    add_variant(candidate)
                    queue.append(candidate)

        for prefix in prefixes:
            if current.startswith(prefix) and len(current) - len(prefix) >= 3:
                candidate = current[len(prefix) :]
                if candidate not in seen:
                    add_variant(candidate)
                    queue.append(candidate)

        for suffix in suffixes:
            if current.endswith(suffix) and len(current) - len(suffix) >= 3:
                candidate = current[: -len(suffix)]
                if candidate not in seen:
                    add_variant(candidate)
                    queue.append(candidate)

    return variants


def load_json_embeddings(
    language: str,
) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
    base_dir = os.getcwd()
    icon_path = os.path.join(
        base_dir, "embeddings", f"icon_embeddings.{language}.json"
    )
    vocab_path = os.path.join(
        base_dir, "embeddings", f"vocab_embeddings.{language}.json"
    )

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


def add_weighted_vector(
    target: List[float], vec: Sequence[float], weight: float
) -> None:
    for i, value in enumerate(vec):
        target[i] += weight * value


def weighted_mean(vectors: List[Tuple[List[float], float]]) -> List[float]:
    if not vectors:
        return []
    dim = len(vectors[0][0])
    sums = [0.0] * dim
    total_weight = 0.0
    for vec, weight in vectors:
        add_weighted_vector(sums, vec, weight)
        total_weight += weight
    if total_weight == 0.0:
        return [0.0] * dim
    return [value / total_weight for value in sums]


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


def _common_prefix_length(word: str, candidate: str) -> int:
    count = 0
    for left_char, right_char in zip(word, candidate):
        if left_char != right_char:
            break
        count += 1
    return count


def _common_suffix_length(word: str, candidate: str) -> int:
    count = 0
    for left_char, right_char in zip(reversed(word), reversed(candidate)):
        if left_char != right_char:
            break
        count += 1
    return count


def _similarity_with_structure(
    word: str,
    candidate: str,
) -> tuple[float, bool]:
    max_len = max(len(word), len(candidate))
    if max_len == 0:
        return 1.0, True

    distance = levenshtein_distance(word, candidate)
    base_similarity = 1.0 - (distance / max_len)

    prefix_len = _common_prefix_length(word, candidate)
    suffix_len = _common_suffix_length(word, candidate)

    prefix_bonus = min(prefix_len, 4) * 0.06
    suffix_bonus = min(suffix_len, 3) * 0.025

    first_char_bonus = 0.0
    same_first_char = False
    if len(word) > 0 and len(candidate) > 0:
        same_first_char = word[0] == candidate[0]
        if same_first_char:
            first_char_bonus = 0.09
        else:
            first_char_bonus = -0.18

    length_ratio = min(len(word), len(candidate)) / max_len
    length_penalty = -0.08 if length_ratio < 0.6 else 0.0

    similarity = (
        base_similarity
        + prefix_bonus
        + suffix_bonus
        + first_char_bonus
        + length_penalty
    )
    similarity = max(0.0, min(similarity, 1.0))

    structural_match = (
        (prefix_len >= 2 and same_first_char)
        or prefix_len >= 3
        or (suffix_len >= 3 and same_first_char)
        or (length_ratio >= 0.85 and same_first_char)
        or base_similarity >= 0.9
    )

    return similarity, structural_match


def get_close_matches(
    word: str,
    possibilities: Iterable[str],
    n: int = 3,
    cutoff: float = 0.6,
    return_scores: bool = False,
) -> List[Tuple[str, float]] | List[str]:
    if not word:
        return []

    word_lower = word.lower()
    scored_matches: List[Tuple[str, float]] = []
    for possibility in possibilities:
        candidate_lower = possibility.lower()
        similarity, structural_match = _similarity_with_structure(
            word_lower,
            candidate_lower,
        )
        if not structural_match:
            continue
        if similarity >= cutoff:
            scored_matches.append((possibility, similarity))
    scored_matches.sort(key=lambda item: item[1], reverse=True)
    top_matches = scored_matches[:n]
    if return_scores:
        return top_matches
    return [match for match, _ in top_matches]


def lookup_token_vector(
    token: str,
    vocab: Dict[str, List[float]],
    language: str | None,
) -> Optional[Tuple[List[float], str]]:
    for variant in normalize_token_variants(token, language):
        if variant in vocab:
            return vocab[variant], variant
    return None


def average_embedding(
    text: str,
    vocab: Dict[str, List[float]],
    stopwords: set[str],
    language: str | None,
    similarity_threshold: float = 0.5,
) -> List[float] | None:
    tokens = tokenize(text, stopwords)
    if not tokens:
        return None

    vectors: List[List[float]] = []
    weighted_vectors: List[Tuple[List[float], float]] = []
    for token in tokens:
        lookup = lookup_token_vector(token, vocab, language)
        if lookup is not None:
            vector, matched_token = lookup
            vectors.append(vector)
            weighted_vectors.append((vector, 1.0))
            if matched_token != token.lower():
                typer.echo(f"Using base '{matched_token}' for '{token}'")
            continue

        close_matches = get_close_matches(
            token,
            vocab.keys(),
            n=2,
            cutoff=similarity_threshold,
            return_scores=True,
        )
        if close_matches:
            match_result = close_matches[0]
            best_word = match_result[0]
            score = match_result[1]
            typer.echo(f"Using '{best_word}' for '{token}'")
            weighted_vectors.append((vocab[best_word], float(score)))
            vectors.append(vocab[best_word])

    if not vectors:
        close_matches = get_close_matches(
            text.lower(),
            vocab.keys(),
            n=1,
            cutoff=0.5,
            return_scores=True,
        )
        if close_matches:
            match_result = close_matches[0]
            word = match_result[0]
            score = match_result[1]
            weighted_vectors.append((vocab[word], float(score)))
        else:
            return None

    if not weighted_vectors:
        return None

    return weighted_mean(weighted_vectors)


def build_icon_index(
    icon_embeds: Dict[str, List[float]]
) -> List[Tuple[str, List[float], float]]:
    index: List[Tuple[str, List[float], float]] = []
    for icon_id, vector in icon_embeds.items():
        norm = vector_norm(vector)
        if norm == 0.0:
            continue
        index.append((icon_id, vector, norm))
    return index


def search_icons(
    query: str,
    icon_index: Sequence[Tuple[str, List[float], float]],
    vocab_embeds: Dict[str, List[float]],
    stopwords: set[str],
    language: str,
    top_k: int = 20,
    use_average_embedding: bool = False,
) -> List[Tuple[str, float]]:
    if use_average_embedding:
        # Use weighted average embedding with fuzzy matching
        query_vec = average_embedding(
            query,
            vocab_embeds,
            stopwords,
            language,
        )
        if query_vec is None:
            return []
    else:
        # Direct word lookup without fuzzy matching or weighted averaging
        tokens = tokenize(query, stopwords)
        if not tokens:
            return []

        vectors: List[List[float]] = []
        for token in tokens:
            lookup = lookup_token_vector(token, vocab_embeds, language)
            if lookup is not None:
                vector, matched_token = lookup
                vectors.append(vector)
                if matched_token != token.lower():
                    typer.echo(f"Using base '{matched_token}' for '{token}'")

        if not vectors:
            return []

        # Simple arithmetic mean (no fuzzy matching, no weighting)
        dim = len(vectors[0])
        query_vec = [
            sum(vec[i] for vec in vectors) / len(vectors) for i in range(dim)
        ]

    query_norm = vector_norm(query_vec)
    if query_norm == 0.0:
        return []

    scored: List[Tuple[str, float]] = []
    for icon_id, icon_vec, icon_norm in icon_index:
        similarity = dot_product(query_vec, icon_vec) / (
            query_norm * icon_norm
        )
        scored.append((icon_id, similarity))

    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:top_k]


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
    use_average_embedding: bool = typer.Option(
        True,
        "--use-average-embedding",
        help="Use weighted average embedding with fuzzy matching (default: False)",
    ),
) -> None:
    project = Project(project_file)
    _ = project.Settings(ProjectSettings)

    icon_embeds, vocab_embeds = load_json_embeddings(language)
    if not icon_embeds:
        raise ValueError(
            "Icon embeddings are empty – run create_icons_embeddings.py first"
        )

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
            use_average_embedding=use_average_embedding,
        )

        if not results:
            typer.echo("No results found.")
            continue

        for icon_id, score in results:
            typer.echo(f"[{score:.3f}]  {icon_id}")


if __name__ == "__main__":
    app()

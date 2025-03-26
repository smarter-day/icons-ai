#!.venv/bin/python

#!/usr/bin/env python3

import concurrent.futures
import json
import dotenv
import numpy as np
import typer
from nltk.corpus import wordnet
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()
app = typer.Typer()

# ====================================================
# CONFIG
# ====================================================
# Move to a specialized model for search/QA:
MODEL_NAME = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
# MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

# Original tags (for icons): Quadratic weighting => weight = (BASE_WEIGHT - i)^2
# Synonyms (including verbs, adjectives, etc.): Linear weighting => weight = (BASE_WEIGHT - j)
# Additionally, synonyms must never exceed (min_orig_weight - 1).
BASE_WEIGHT = 10

# We'll retrieve synonyms, verbs, adjectives, etc., and possibly n-grams
SYNONYMS_COUNT = 1
SYNONYMS_SIMILARITY_THRESHOLD = 0.8  # filter out synonyms below this cosine similarity

# "Generic" icon penalty thresholds
AVG_THRESHOLD = 0.35
STD_THRESHOLD = 0.10
TOP_DIFF_THRESHOLD = 0.08

# Weighted Overlap alpha & beta (for final icon–category score)
ALPHA = 0.8   # portion from cosine similarity
BETA  = 0.2   # portion from token overlap (Jaccard)

# ====================================================
# GLOBALS (lazy model init in each worker process)
# ====================================================
_global_model = None
def get_model():
    """
    Lazily load the embedding model in each process.
    """
    global _global_model
    if _global_model is None:
        _global_model = SentenceTransformer(MODEL_NAME)
    return _global_model

# ====================================================
# COSINE SIMILARITY
# ====================================================
def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denom == 0.0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)

# ====================================================
# GENERIC PENALTY
# ====================================================
def generic_penalty_factor(similarities: list[float]) -> float:
    """
    If the icon is generically similar to many categories,
    we reduce its final scores accordingly.
    """
    if not similarities:
        return 1.0

    avg_sim = float(np.mean(similarities))
    std_sim = float(np.std(similarities))
    sorted_sims = sorted(similarities, reverse=True)

    top_diff = 0.0
    if len(sorted_sims) > 1:
        top_diff = float(sorted_sims[0] - sorted_sims[1])

    penalty = 1.0
    # If average similarity is high => reduce
    if avg_sim > AVG_THRESHOLD:
        penalty *= 0.85
    # If std dev is low => reduce
    if std_sim < STD_THRESHOLD:
        penalty *= 0.85
    # If difference between top 1 and top 2 is small => reduce
    if top_diff < TOP_DIFF_THRESHOLD:
        penalty *= 0.85

    return penalty

# ====================================================
# UTILITY: N-GRAMS
# ====================================================
def generate_ngrams(words: list[str], n: int) -> list[str]:
    """
    Generate contiguous n-grams from a list of tokens.
    e.g. words=['task','management','app'], n=2 => ['task management', 'management app']
    """
    if len(words) < n:
        return []
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

def phrase_expansions(tag: str) -> list[str]:
    """
    Basic approach: produce bigrams/trigrams from the tag itself if multi-word.
    E.g. 'project management' => tokens=['project','management'] => bigrams => same in this case
    """
    tokens = tag.strip().lower().split()
    expansions = [tag.lower()]  # keep original
    # generate bigrams, trigrams
    expansions.extend(generate_ngrams(tokens, 2))
    expansions.extend(generate_ngrams(tokens, 3))
    expansions = list(set(expansions))  # deduplicate
    return expansions

# ====================================================
# GET SYNONYMS + VERBS (plus n-grams expansions)
# ====================================================
def get_expanded_similar_words(tag: str, max_synonyms: int = SYNONYMS_COUNT) -> list[str]:
    tag = tag.strip().lower()
    if not tag:
        return []

    # Basic expansions (n-grams of original)
    expansions = set(phrase_expansions(tag))

    model = get_model()
    tag_emb = model.encode(tag, convert_to_numpy=True)

    # Gather synonyms for all relevant POS
    # (use the same code path instead of separate blocks)
    POS_TYPES = [wordnet.NOUN, wordnet.VERB, wordnet.ADJ, wordnet.ADV]
    syns = set()
    for pos_type in POS_TYPES:
        for synset in wordnet.synsets(tag, pos=pos_type):
            for lemma in synset.lemmas():
                cand = lemma.name().replace("_", " ").lower()
                if cand != tag:
                    syns.add(cand)

    expansions.update(syns)

    # Score and filter by similarity
    scored = []
    for cand in expansions:
        cand_emb = model.encode(cand, convert_to_numpy=True)
        score = cosine_similarity(tag_emb, cand_emb)
        if score >= SYNONYMS_SIMILARITY_THRESHOLD:
            scored.append((cand, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scored[:max_synonyms]]

# ====================================================
# ICON TEXT BUILDER
# ====================================================
def build_icon_text_and_synonyms(icon_item: dict) -> tuple[str, list[str]]:
    """
    1) Sort original tags by similarity to icon name => Quadratic weighting
    2) For each original tag => expand with synonyms, verbs, n-grams => linear weighting (never > min_orig_weight-1)
    3) Weighted overlap not applied here; we'll do it in final scoring.
    4) Append icon_name once
    """
    model = get_model()
    icon_name = icon_item.get("name", "").strip()
    raw_tags = icon_item.get("tags", "").strip()
    original_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    # embed icon name if present
    if icon_name:
        name_emb = model.encode(icon_name.lower(), convert_to_numpy=True)
    else:
        name_emb = None

    # 1) Sort original tags by similarity
    orig_list = []
    for tag in original_tags:
        if name_emb is not None and tag:
            tag_emb = model.encode(tag.lower(), convert_to_numpy=True)
            sim = cosine_similarity(name_emb, tag_emb)
        else:
            sim = 0.0
        orig_list.append((tag, sim))

    orig_list.sort(key=lambda x: x[1], reverse=True)

    text_for_embedding = []
    final_tokens = []

    # Quadratic weighting for original tags
    for i, (tag, sim) in enumerate(orig_list):
        weight = (BASE_WEIGHT - i)**2
        if weight < 1:
            weight = 1
        text_for_embedding.extend([tag]*weight)
        final_tokens.append(tag)

    # find smallest original tag weight
    if len(orig_list) > 0:
        i_last = len(orig_list) - 1
        min_orig_weight = (BASE_WEIGHT - i_last)**2
        if min_orig_weight < 1:
            min_orig_weight = 1
    else:
        min_orig_weight = 1

    # 2) synonyms from all original tags
    syn_candidates = []
    for tag, _ in orig_list:
        expansions = get_expanded_similar_words(tag, max_synonyms=SYNONYMS_COUNT)
        # measure each expansion's similarity to icon_name
        for syn in expansions:
            if name_emb is not None:
                syn_emb = model.encode(syn.lower(), convert_to_numpy=True)
                s_score = cosine_similarity(name_emb, syn_emb)
            else:
                s_score = 0.0
            syn_candidates.append((syn, s_score))

    # sort synonyms by desc
    syn_candidates.sort(key=lambda x: x[1], reverse=True)

    # linear weighting but never exceed (min_orig_weight - 1)
    max_syn_weight = int(min_orig_weight - 1)
    if max_syn_weight < 1:
        max_syn_weight = 1

    syn_index = 0
    for (syn, s_score) in syn_candidates:
        w_syn = (BASE_WEIGHT - syn_index)
        if w_syn < 1:
            w_syn = 1
        if w_syn > max_syn_weight:
            w_syn = max_syn_weight

        text_for_embedding.extend([syn]*w_syn)
        final_tokens.append(syn)
        syn_index += 1

    # 3) Append icon_name once
    if icon_name:
        text_for_embedding = [icon_name] * BASE_WEIGHT + text_for_embedding

    embed_text = " ".join(text_for_embedding)
    return embed_text, final_tokens

# ====================================================
# WEIGHTED OVERLAP - COMBINE COSINE + JACCARD
# ====================================================
def compute_final_score(icon_tokens: list[str], cat_tokens: list[str], cos_score: float) -> float:
    """
    Weighted Overlap approach:
      final = ALPHA*cos_score + BETA*jaccard(icon_tokens, cat_tokens)
    icon_tokens and cat_tokens are sets or lists. We'll convert to sets for overlap.
    """
    icon_set = set(icon_tokens)
    cat_set = set(cat_tokens)
    if not icon_set or not cat_set:
        return cos_score

    intersection = icon_set.intersection(cat_set)
    union = icon_set.union(cat_set)
    if not union:
        jaccard = 0.0
    else:
        jaccard = len(intersection) / len(union)

    return ALPHA * cos_score + BETA * jaccard

# ====================================================
# ENRICH ICON
# ====================================================
def enrich_icon(icon_item: dict, category_data_embs: dict[str, tuple[str, np.ndarray]]) -> dict:
    """
    1) build icon text => embed
    2) for each category => use Weighted Overlap
    3) apply generic penalty => final
    """
    # (1) Build final text + tokens
    icon_text, final_tokens_sorted = build_icon_text_and_synonyms(icon_item)
    model = get_model()
    icon_emb = model.encode(icon_text, convert_to_numpy=True)

    # We'll store cos sims to apply generic penalty
    cos_sims = []

    # We'll produce final cat score with Weighted Overlap
    cat_scores = {}
    for cat_name, (cat_text, cat_emb) in category_data_embs.items():
        # cos
        cos_score = cosine_similarity(icon_emb, cat_emb)
        cos_sims.append(cos_score)

        # Weighted Overlap
        # cat_text => to get tokens
        cat_tokens = set(cat_text.split())
        final_score = compute_final_score(final_tokens_sorted, list(cat_tokens), cos_score)

        cat_scores[cat_name] = final_score

    # generic penalty
    penalty = generic_penalty_factor(cos_sims)

    final_cats = {}
    for c_name, raw_score in cat_scores.items():
        final_cats[c_name] = raw_score * penalty

    # best cat
    best_cat = None
    best_score = float("-inf")
    for c_name, val in final_cats.items():
        if val > best_score:
            best_score = val
            best_cat = c_name

    icon_enriched = dict(icon_item)
    icon_enriched["categories"] = final_cats
    icon_enriched["score"] = best_score
    icon_enriched["top_category"] = best_cat
    # remove duplicates
    icon_enriched["keywords"] = {"en": list(set(final_tokens_sorted))}
    return icon_enriched

# ====================================================
# BUILD CATEGORY EMBEDDINGS (plus token sets for Weighted Overlap)
# ====================================================
def build_weighted_category_text(cat_name: str, cat_info: dict) -> str:
    """
    1) Sort the category's keywords by similarity to cat_name.
    2) Weighted approach => (BASE_WEIGHT - i).
    3) Then append cat_name + audience.
    """
    model = get_model()

    # embed cat_name
    cat_emb = model.encode(cat_name, convert_to_numpy=True)

    # gather keywords
    keywords = cat_info.get("keywords", [])
    scored_keywords = []
    for kw in keywords:
        kw_emb = model.encode(kw, convert_to_numpy=True)
        sim = cosine_similarity(cat_emb, kw_emb)
        scored_keywords.append((kw, sim))

    # sort desc
    scored_keywords.sort(key=lambda x: x[1], reverse=True)

    tokens = []
    for i, (kw, _) in enumerate(scored_keywords):
        w = max(1, BASE_WEIGHT - i)
        tokens.extend([kw]*w)

    # cat_name
    # tokens.append(cat_name)

    # audience
    # aud = cat_info.get("audience", [])
    # if aud:
    #     tokens.append(" ".join(aud))

    return " ".join(tokens)

# ====================================================
# MAIN
# ====================================================
@app.command()
def main(
    icons_file: str = typer.Option(..., help="Path to icons JSON"),
    categories_file: str = typer.Option(..., help="Path to categories JSON"),
    output_file: str = typer.Option(..., help="Output JSON file"),
    max_workers: int = typer.Option(None, help="Number of parallel processes")
):
    """
    Enhanced for best similarity:
      - Uses multi-qa-mpnet-base-dot-v1
      - Adds phrase-level expansions (n-grams)
      - Weighted Overlap approach (cosine + Jaccard)
    """
    try:
        _ = wordnet.synsets("example")
    except LookupError:
        typer.echo("Missing NLTK WordNet data. Please install:\npython -m nltk.downloader wordnet")
        raise typer.Exit()

    typer.echo(f"Loading icons from {icons_file}")
    with open(icons_file, "r", encoding="utf-8") as f:
        icons_data = json.load(f)

    typer.echo(f"Loading categories from {categories_file}")
    with open(categories_file, "r", encoding="utf-8") as f:
        categories_data = json.load(f)

    typer.echo(f"Pre-loading model: {MODEL_NAME}")
    parent_model = SentenceTransformer(MODEL_NAME)

    # Build category embeddings + raw text (for Weighted Overlap)
    category_data_embs = {}
    typer.echo("Building category data with sorted keywords + embeddings...")

    for cat_name, cat_info in categories_data.items():
        cat_text = build_weighted_category_text(cat_name, cat_info)
        cat_emb = parent_model.encode(cat_text, convert_to_numpy=True)
        category_data_embs[cat_name] = (cat_text, cat_emb)

    icons_list = icons_data["icons"]
    typer.echo("Enriching icons in parallel with synonyms, verbs, n-grams...")

    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        tasks = (executor.submit(enrich_icon, icon, category_data_embs) for icon in icons_list)
        enriched_icons = [t.result() for t in concurrent.futures.as_completed(tasks)]

    # sort final icons by (top_category asc, score desc)
    def sort_key(ic):
        return (ic["top_category"], -ic["score"])
    enriched_icons.sort(key=sort_key)

    # build final
    final_data = {"icons": enriched_icons}
    typer.echo(f"Saving results to {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2)

    typer.echo("Done.")

if __name__ == "__main__":
    app()

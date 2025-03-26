#!.venv/bin/python

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
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"

# Original tags (for icons): Quadratic weighting => weight = (BASE_WEIGHT - i)^2
# Synonyms: Linear weighting => weight = (BASE_WEIGHT - j)
# Additionally, synonyms must never exceed (min_orig_weight - 1).
BASE_WEIGHT = 10

# We'll retrieve many synonyms, but also gather the same amount of verbs
# to handle search queries that use verbs. Combined total can be large, but
# synonyms will be sorted by similarity and still have lower weighting.
SYNONYMS_COUNT = 200

# "Generic" icon penalty thresholds
AVG_THRESHOLD = 0.35
STD_THRESHOLD = 0.10
TOP_DIFF_THRESHOLD = 0.08

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
    avg_sim = float(np.mean(similarities))
    std_sim = float(np.std(similarities))
    sorted_sims = sorted(similarities, reverse=True)
    top_diff = float(sorted_sims[0] - sorted_sims[1]) if len(sorted_sims) > 1 else 0.0

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
# GET SYNONYMS + VERBS
# ====================================================
def get_similar_words_for_tags(tag: str, max_synonyms: int = SYNONYMS_COUNT) -> list[str]:
    """
    Retrieve synonyms for `tag` from WordNet (same POS as the first synset),
    then also gather up to `max_synonyms` synonyms that are specifically VERBs.
    Rank them all by their similarity to `tag` and return them combined.

    Skips multi-word original tags. If the first synset is a verb, we'll still
    gather noun synonyms by default (or whichever the first synset is).
    We unify the sets, remove duplicates, then sort.
    """

    tag_clean = tag.strip().lower()
    if not tag_clean or " " in tag_clean:
        return []

    model = get_model()
    tag_emb = model.encode(tag_clean, convert_to_numpy=True)

    # Identify first synset's POS, gather synonyms for that
    synsets = wordnet.synsets(tag_clean)
    if not synsets:
        return []
    first_pos = synsets[0].pos()  # e.g. 'n', 'v', etc.

    # 1) synonyms for the first_pos
    samepos_candidates = set()
    for syn in synsets:
        if syn.pos() == first_pos:
            for lemma in syn.lemmas():
                cand = lemma.name().replace("_", " ").strip().lower()
                if cand != tag_clean:
                    samepos_candidates.add(cand)

    # 2) synonyms specifically for verbs
    #    Even if first_pos is 'v', this ensures we gather a separate set of verb synonyms
    #    (the user wants the same amount of verbs).
    verb_candidates = set()
    all_synsets_for_verbs = wordnet.synsets(tag_clean, pos=wordnet.VERB)  # force pos='v'
    for syn in all_synsets_for_verbs:
        for lemma in syn.lemmas():
            cand = lemma.name().replace("_", " ").strip().lower()
            if cand != tag_clean:
                verb_candidates.add(cand)

    # Combine them
    combined_candidates = samepos_candidates.union(verb_candidates)

    # 3) synonyms specifically for adjectives
    adj_candidates = set()
    all_synsets_for_verbs = wordnet.synsets(tag_clean, pos=wordnet.ADJ) # adjectives
    for syn in all_synsets_for_verbs:
        for lemma in syn.lemmas():
            cand = lemma.name().replace("_", " ").strip().lower()
            if cand != tag_clean:
                adj_candidates.add(cand)

    # Combine them
    combined_candidates = combined_candidates.union(adj_candidates)

    # 4) synonyms specifically for adjectives
    adj_candidates = set()
    all_synsets_for_verbs = wordnet.synsets(tag_clean, pos=wordnet.ADJ_SAT) # adjectives
    for syn in all_synsets_for_verbs:
        for lemma in syn.lemmas():
            cand = lemma.name().replace("_", " ").strip().lower()
            if cand != tag_clean:
                adj_candidates.add(cand)

    # Combine them
    combined_candidates = combined_candidates.union(adj_candidates)

    # 5) synonyms specifically for adverbs
    adv_candidates = set()
    all_synsets_for_verbs = wordnet.synsets(tag_clean, pos=wordnet.ADV)
    for syn in all_synsets_for_verbs:
        for lemma in syn.lemmas():
            cand = lemma.name().replace("_", " ").strip().lower()
            if cand != tag_clean:
                adv_candidates.add(cand)

    # Combine them
    combined_candidates = combined_candidates.union(adv_candidates)

    if not combined_candidates:
        return []

    # Rank by similarity to the original tag
    scored = []
    for cand in combined_candidates:
        cand_emb = model.encode(cand, convert_to_numpy=True)
        score = cosine_similarity(tag_emb, cand_emb)
        scored.append((cand, score))

    # sort descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # We'll pick up to 2*max_synonyms because we gather synonyms for both sets
    # (the user says they'd like the same amount for each, we can do 2x total).
    top_final = scored[:max_synonyms]
    # Return just the text
    return [x[0] for x in top_final]

# ====================================================
# ICON TEXT BUILDER
# ====================================================
def build_icon_text_and_synonyms(icon_item: dict) -> tuple[str, list[str]]:
    """
    Steps:
     1) Parse icon name & raw comma-separated tags.
     2) Sort original tags by similarity to icon name => Quadratic weighting => (BASE_WEIGHT - i)^2
     3) Gather synonyms+verbs from all original tags => measure similarity => sort => linear weighting => (BASE_WEIGHT - j)
        BUT never exceed (min_orig_weight - 1).
     4) Repeat each token in final text that many times; synonyms get smaller weighting.
     5) Append icon_name once if present.
     6) Return (embedding_text, final_tokens_in_order).
    """
    model = get_model()
    icon_name = icon_item.get("name", "").strip()
    raw_tags = icon_item.get("tags", "").strip()
    original_tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    # 1) Sort original tags by similarity to icon name
    if icon_name:
        name_emb = model.encode(icon_name.lower(), convert_to_numpy=True)
    else:
        name_emb = None

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
        weight = (BASE_WEIGHT - i) ** 2
        if weight < 1:
            weight = 1
        text_for_embedding.extend([tag] * weight)
        final_tokens.append(tag)

    # min_orig_weight
    if orig_list:
        i_last = len(orig_list) - 1
        min_orig_weight = (BASE_WEIGHT - i_last) ** 2
        if min_orig_weight < 1:
            min_orig_weight = 1
    else:
        min_orig_weight = 1

    # 2) synonyms+verbs from all original tags
    syn_candidates = []
    for tag, _ in orig_list:
        tag_syn_verb = get_similar_words_for_tags(tag, max_synonyms=SYNONYMS_COUNT)
        # We'll measure each's similarity to icon_name
        for syn in tag_syn_verb:
            if name_emb is not None:
                syn_emb = model.encode(syn.lower(), convert_to_numpy=True)
                s_score = cosine_similarity(name_emb, syn_emb)
            else:
                s_score = 0.0
            syn_candidates.append((syn, s_score))

    # Sort synonyms (including verbs) by desc similarity
    syn_candidates.sort(key=lambda x: x[1], reverse=True)

    # We'll apply linear weighting (BASE_WEIGHT - j)
    # but never exceed (min_orig_weight - 1)
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

        text_for_embedding.extend([syn] * w_syn)
        final_tokens.append(syn)
        syn_index += 1

    # 3) Append icon_name once
    if icon_name:
        text_for_embedding.append(icon_name)

    embed_text = " ".join(text_for_embedding)
    return embed_text, final_tokens

# ====================================================
# ENRICH ICON
# ====================================================
def enrich_icon(icon_item: dict, category_embeddings: dict[str, np.ndarray]) -> dict:
    """
    - Build final text using build_icon_text_and_synonyms().
    - Encode => compare with categories => apply penalty => find best cat => store.
    """
    icon_text, final_tokens_sorted = build_icon_text_and_synonyms(icon_item)
    model = get_model()
    icon_emb = model.encode(icon_text, convert_to_numpy=True)

    cat_scores = {}
    sims = []
    for cat_name, cat_emb in category_embeddings.items():
        sc = cosine_similarity(icon_emb, cat_emb)
        cat_scores[cat_name] = sc
        sims.append(sc)

    # apply generic penalty
    penalty = generic_penalty_factor(sims)
    final_cats = {}
    for c_name, sc in cat_scores.items():
        final_cats[c_name] = sc * penalty

    # find best cat
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
    icon_enriched["keywords"] = {"en": list(set(final_tokens_sorted))}
    return icon_enriched

# ====================================================
# CATEGORY EMBEDDINGS (SORTED KEYWORDS)
# ====================================================
def build_weighted_category_text(cat_name: str, cat_info: dict) -> str:
    """
    1) Sort the category's keywords by similarity to cat_name.
    2) Weighted approach => (BASE_WEIGHT - i).
    3) Then append cat_name + audience.
    """
    model = get_model()

    # Embed cat_name
    cat_emb = model.encode(cat_name, convert_to_numpy=True)

    # Gather keywords & compute similarity
    keywords = cat_info.get("keywords", [])
    scored_keywords = []
    for kw in keywords:
        kw_emb = model.encode(kw, convert_to_numpy=True)
        sim = cosine_similarity(cat_emb, kw_emb)
        scored_keywords.append((kw, sim))

    # Sort desc by similarity to cat_name
    scored_keywords.sort(key=lambda x: x[1], reverse=True)

    tokens = []
    for i, (kw, sim) in enumerate(scored_keywords):
        w = max(1, BASE_WEIGHT - i)
        tokens.extend([kw] * w)

    # Append cat_name itself
    tokens.append(cat_name)

    # Then audience (unweighted)
    aud = cat_info.get("audience", [])
    if aud:
        tokens.append(" ".join(aud))

    return " ".join(tokens)

# ====================================================
# MAIN CLI
# ====================================================
@app.command()
def main(
    icons_file: str = typer.Option(..., help="Path to icons JSON file"),
    categories_file: str = typer.Option(..., help="Path to categories JSON file"),
    output_file: str = typer.Option(..., help="Path to output JSON file"),
    max_workers: int = typer.Option(None, help="Number of parallel workers"),
):
    """
    1) For each category:
       - Sort keywords by similarity to cat_name => (BASE_WEIGHT - i) weighting => embed that text as the category embedding.

    2) For each icon:
       - Sort original tags by similarity to icon_name => Quadratic weighting
       - Gather synonyms & verbs => linear weighting, never exceeding (min_orig_weight - 1)
       - Append icon_name once
       => embed => measure similarity to categories => apply 'generic' penalty => find top_category

    3) Sort final icons by (top_category asc, score desc)
    4) Output final JSON
    """

    # Ensure NLTK WordNet
    try:
        _ = wordnet.synsets("example")
    except LookupError:
        typer.echo("Missing WordNet data. Please run: python -m nltk.downloader wordnet")
        raise typer.Exit()

    typer.echo(f"Loading icons: {icons_file}")
    with open(icons_file, "r", encoding="utf-8") as f:
        icons_data = json.load(f)

    typer.echo(f"Loading categories: {categories_file}")
    with open(categories_file, "r", encoding="utf-8") as f:
        categories_data = json.load(f)

    typer.echo(f"Pre-loading model: {MODEL_NAME}")
    parent_model = SentenceTransformer(MODEL_NAME)

    # Build sorted (by similarity) embeddings for categories
    typer.echo("Building category embeddings with sorted keywords...")
    category_embeddings = {}
    for cat_name, cat_info in categories_data.items():
        cat_text = build_weighted_category_text(cat_name, cat_info)
        cat_emb = parent_model.encode(cat_text, convert_to_numpy=True)
        category_embeddings[cat_name] = cat_emb

    icons_list = icons_data["icons"]
    typer.echo("Processing icons in parallel...")

    # Parallel enrichment
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        tasks = (executor.submit(enrich_icon, icon, category_embeddings) for icon in icons_list)
        enriched_icons = [t.result() for t in concurrent.futures.as_completed(tasks)]

    # Sort final icons by (top_category asc, score desc)
    def sort_key(icon):
        return (icon["top_category"], -icon["score"])

    enriched_icons.sort(key=sort_key)

    # Prepare final JSON
    final_result = {"icons": enriched_icons}
    typer.echo(f"Saving to: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_result, f, indent=2)

    typer.echo("Done.")

if __name__ == "__main__":
    app()

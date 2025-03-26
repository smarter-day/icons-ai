#!/usr/bin/env python

import os
import json
import numpy as np
import dotenv
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()

# Configuration
# MODEL_NAME = "distiluse-base-multilingual-cased-v2"  # Supports English + Russian
MODEL_NAME = os.environ.get("EMBEDDING_MODEL")
# MODEL_NAME = "nomic-ai/nomic-embed-text-v1"  # Supports English + Russian
ICONS_JSON_FILE = "../../data/icons.json"  # Input file with icon tags
OUTPUT_EMBEDDINGS_FILE = "../../data/icon_embeddings.npy"  # Output embeddings
OUTPUT_EMBEDDINGS_FILE_JSON = "../data/icon_embeddings.json"  # Output embeddings
OUTPUT_ICONS_INDEX = "data/icons_index.json"  # Output metadata

def generate_embeddings():
    # Load the SentenceTransformer model
    print(f"Loading model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME, trust_remote_code=True)
    print("Model loaded.")

    # Load icons data
    print(f"Loading icons from {ICONS_JSON_FILE}...")
    with open(ICONS_JSON_FILE, "r", encoding="utf-8") as f:
        icons_data = json.load(f)

    icons = icons_data["icons"]
    print(f"Total icons found: {len(icons)}")

    # Generate embeddings for each icon's tags
    print("Embedding icons...")
    icon_embeddings = []
    icon_metadata = []
    for icon in icons:
        tags = icon["tags"]
        terms = icon["name"] + tags
        embedding = model.encode(terms, convert_to_numpy=True)  # Generate embedding
        icon_embeddings.append(embedding)
        icon_metadata.append({"id": icon["name"], "tags": terms})  # Store minimal metadata

    # Save embeddings and metadata
    icon_embeddings = np.array(icon_embeddings)
    np.save(OUTPUT_EMBEDDINGS_FILE, icon_embeddings)
    print(f"Embeddings saved to: {OUTPUT_EMBEDDINGS_FILE}")

    with open(OUTPUT_ICONS_INDEX, "w", encoding="utf-8") as f:
        json.dump(icon_metadata, f, ensure_ascii=False, indent=2)
    print(f"Icon metadata saved to: {OUTPUT_ICONS_INDEX}")

    embeddings = np.load(OUTPUT_EMBEDDINGS_FILE)

    # Convert to a list of lists (JSON-compatible)
    embeddings_list = embeddings.tolist()

    # Save to JSON
    with open(OUTPUT_EMBEDDINGS_FILE_JSON, "w") as f:
        json.dump(embeddings_list, f)

    print("Converted icon_embeddings.npy to icon_embeddings.json")

    print("Done.")

if __name__ == "__main__":
    generate_embeddings()
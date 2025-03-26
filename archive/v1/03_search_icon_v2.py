import numpy as np
import json
import os
import dotenv
from model2vec import StaticModel

dotenv.load_dotenv()

MODEL_NAME = os.environ.get("EMBEDDING_MODEL", "cnmoro/multilingual-e5-small-distilled-16m")

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def load_data():
    embeddings = np.array(json.load(open("../data/icon_embeddings.json", "r")))
    metadata = json.load(open("../../data/icons_index.json", "r"))
    return embeddings, metadata

def find_best_match(query_embedding, embeddings, metadata):
    similarities = [cosine_similarity(query_embedding, emb) for emb in embeddings]
    best_idx = int(np.argmax(similarities))
    return metadata[best_idx], similarities[best_idx]

if __name__ == "__main__":
    embeddings, metadata = load_data()

    # Load the model for encoding the query
    print(f"Loading model '{MODEL_NAME}' for query embedding...")
    model = StaticModel.from_pretrained(MODEL_NAME)
    print("Model loaded.")

    query = input("Enter search: ")
    # Compute the query embedding (ensure it outputs a numpy array)
    query_embedding = model.encode([query], convert_to_numpy=True)[0]

    best_match, score = find_best_match(query_embedding, embeddings, metadata)
    print("Best match:", best_match)
    print("Score:", score)

import os

import onnxruntime as ort
import numpy as np
from transformers import AutoTokenizer
from scipy.spatial.distance import cosine
import json
import dotenv

dotenv.load_dotenv()

# Load the ONNX model
ort_session = ort.InferenceSession("../../data/multilingual_e5_quantized.onnx")

# Load the tokenizer with the corrected model name
tokenizer = AutoTokenizer.from_pretrained(os.environ.get("EMBEDDING_MODEL"))

# Load precomputed icon embeddings and metadata
icon_embeddings = np.load("../../data/icon_embeddings.npy")  # Shape: (num_icons, embedding_dim)
with open("../../data/icons_index.json", "r", encoding="utf-8") as f:
    icon_metadata = json.load(f)  # List of dictionaries with "id" and "tags"

# Function to generate an embedding from text
def get_embedding(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="np", padding="max_length", max_length=128, truncation=True)
    input_ids = inputs["input_ids"].astype(np.int64)  # Shape: (1, 128)
    attention_mask = inputs["attention_mask"].astype(np.int64)  # Shape: (1, 128)

    # Run inference with the ONNX model
    ort_inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
    embedding = ort_session.run(None, ort_inputs)[0]  # Output shape: (1, embedding_dim)
    return embedding.flatten()  # Flatten to 1D array: (embedding_dim,)

# Function to search icons based on a query
def search_icons(query, top_k=5):
    # Generate embedding for the user query
    query_embedding = get_embedding(query)

    # Compute cosine similarity between query and icon embeddings
    similarities = []
    for icon_emb in icon_embeddings:
        sim = 1 - cosine(query_embedding, icon_emb)  # 1 - cosine distance = similarity
        similarities.append(sim)

    # Get the top-k most similar icons
    top_indices = np.argsort(similarities)[::-1][:top_k]  # Sort descending, take top_k
    results = [icon_metadata[i] for i in top_indices]
    return results

# Example usage
user_query = input("Enter some search term: ")
results = search_icons(user_query)
for icon in results:
    print(f"Icon: {icon['id']}, Data: {icon}")
import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading FAISS index...")
index = faiss.read_index("knowledge_base/faiss_index.index")

print("Loading chunks...")
with open("knowledge_base/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# Ask the user a question
query = input("Enter your question: ")

# Generate embedding
query_embedding = model.encode([query])
query_embedding = np.array(query_embedding).astype("float32")

# Search FAISS
distances, indices = index.search(query_embedding, k=1)

best_match = chunks[indices[0][0]]

print("\n===== Best Match =====")
print("Question :", best_match["question"])
print("Answer   :", best_match["answer"])
print("Source   :", best_match["source"])
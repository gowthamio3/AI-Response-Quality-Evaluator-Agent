import json
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("knowledge_base/faiss_index.index")

# Load chunks
with open("knowledge_base/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)


def retrieve_reference(question):
    embedding = model.encode([question])
    embedding = np.array(embedding).astype("float32")

    distances, indices = index.search(embedding, k=1)

    best = chunks[indices[0][0]]

    return {
        "question": best["question"],
        "answer": best["answer"],
        "source": best["source"]
    }
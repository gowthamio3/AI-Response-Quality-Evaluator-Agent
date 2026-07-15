import json
import pickle
import faiss
import numpy as np

print("Loading embeddings...")

# Load embeddings
with open("knowledge_base/embeddings.pkl", "rb") as file:
    embeddings = pickle.load(file)

# Load chunks
with open("knowledge_base/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

# Convert embeddings to NumPy array
embeddings = np.array(embeddings).astype("float32")

print(f"Loaded {len(embeddings)} embeddings.")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings
index.add(embeddings)

# Save index
faiss.write_index(index, "knowledge_base/faiss_index.index")

print("\n✅ Vector Database Created Successfully!")
print(f"Total vectors stored: {index.ntotal}")
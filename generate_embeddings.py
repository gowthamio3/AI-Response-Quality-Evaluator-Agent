import json
import pickle
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load chunks
with open("knowledge_base/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

print(f"Loaded {len(chunks)} chunks.")

texts = []

# Combine question, context, and answer into one text
for chunk in chunks:
    text = (
        chunk["question"] + " " +
        chunk["context"] + " " +
        chunk["answer"]
    )
    texts.append(text)

print("Generating embeddings...")

embeddings = model.encode(texts, show_progress_bar=True)

# Save embeddings
with open("knowledge_base/embeddings.pkl", "wb") as file:
    pickle.dump(embeddings, file)

print(f"\n✅ Generated {len(embeddings)} embeddings.")
print("✅ Saved as knowledge_base/embeddings.pkl")
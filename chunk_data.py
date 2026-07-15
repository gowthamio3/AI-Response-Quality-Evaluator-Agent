from datasets import load_dataset
import json

print("Loading datasets...")

# Load datasets
squad = load_dataset("squad", download_mode="reuse_dataset_if_exists")

truthfulqa = load_dataset(
    "truthfulqa/truthful_qa",
    "generation",
    download_mode="reuse_dataset_if_exists"
)

chunks = []
# -------- SQuAD --------
for item in squad["train"].select(range(100)):
    chunk= {
        "source": "SQuAD",
        "question": item["question"],
        "context": item["context"],
        "answer": item["answers"]["text"][0] if item["answers"]["text"] else ""
    }
    chunks.append(chunk)

# -------- TruthfulQA --------
for item in truthfulqa["validation"]:
    chunk = {
        "source": "TruthfulQA",
        "question": item["question"],
        "context": "",
        "answer": item["best_answer"]
    }
    chunks.append(chunk)
# -------- AI Knowledge Base --------
with open("datasets/ai_knowledge_base.json", "r", encoding="utf-8") as file:
    ai_data = json.load(file)

for item in ai_data:
    chunk = {
        "source": "AI Knowledge Base",
        "question": item["question"],
        "context": "",
        "answer": item["answer"]
    }
    chunks.append(chunk)

print(f"\n✅ Total Chunks Created: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0])
import json

# Save chunks to a JSON file
with open("knowledge_base/chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4, ensure_ascii=False)

print("\n✅ Chunks saved successfully!")
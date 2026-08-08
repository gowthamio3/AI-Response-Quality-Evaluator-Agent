from datasets import load_dataset

print("Downloading TruthfulQA...")

truthfulqa = load_dataset("truthfulqa/truthful_qa", "generation")

print("TruthfulQA downloaded successfully!")

print(truthfulqa)
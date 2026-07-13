from datasets import load_dataset

print("Downloading SQuAD...")

squad = load_dataset("squad")

print("Downloaded Successfully!")

print(squad)
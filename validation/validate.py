import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.relevance_agent import evaluate_relevance
from agents.accuracy_agent import evaluate_accuracy
from agents.hallucination_agent import detect_hallucination

# Test cases
test_cases = [
    {
        "question": "What is Artificial Intelligence?",
        "response": "Artificial Intelligence is a field of computer science that enables machines to perform tasks requiring human intelligence.",
        "reference": "Artificial Intelligence is a branch of computer science that enables machines to perform tasks requiring human intelligence."
    },
    {
        "question": "What is the capital of India?",
        "response": "The capital of India is Delhi.",
        "reference": "The capital of India is New Delhi."
    },
    {
        "question": "Who invented Artificial Intelligence?",
        "response": "Artificial Intelligence was invented in India in 2010.",
        "reference": "The term Artificial Intelligence was coined by John McCarthy in 1956."
    }
]

for i, test in enumerate(test_cases, start=1):
    print(f"\n========== Test Case {i} ==========")

    print(evaluate_relevance(test["question"], test["response"]))
    print(evaluate_accuracy(
        test["question"],
        test["response"],
        test["reference"]
    ))
    print(detect_hallucination(
        test["question"],
        test["response"],
        test["reference"]
    ))
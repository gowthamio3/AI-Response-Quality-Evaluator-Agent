from agents.verdict_agent import evaluate_verdict

result = evaluate_verdict(
    relevance=8,
    accuracy=7,
    completeness=5,
    hallucination=9
)

print(result)
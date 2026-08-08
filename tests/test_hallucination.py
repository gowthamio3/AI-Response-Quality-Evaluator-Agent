from agents.hallucination_agent import detect_hallucination

question = "What is Artificial Intelligence?"

reference = "Artificial Intelligence is a branch of computer science that enables machines to perform tasks requiring human intelligence."

response = "Artificial Intelligence was invented in India in 2010."

result = detect_hallucination(question, response, reference)

print(result)
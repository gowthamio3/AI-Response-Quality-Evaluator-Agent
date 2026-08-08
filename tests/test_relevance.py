from agents.relevance_agent import evaluate_relevance

question = "What is Artificial Intelligence?"

response = "Artificial Intelligence is a field of computer science that enables machines to learn and solve problems."

result = evaluate_relevance(question, response)

print(result)
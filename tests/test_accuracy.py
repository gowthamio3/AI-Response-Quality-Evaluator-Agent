from agents.accuracy_agent import evaluate_accuracy

question = "What is Artificial Intelligence?"

reference = "Artificial Intelligence is a branch of computer science that enables machines to perform tasks requiring human intelligence."

response = "Artificial Intelligence is a field of computer science that enables machines to learn and solve problems."

result = evaluate_accuracy(question, response, reference)

print(result)
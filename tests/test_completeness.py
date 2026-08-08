from agents.completeness_agent import evaluate_completeness

question = "What is Artificial Intelligence?"

reference = """
Artificial Intelligence (AI) is the simulation of human intelligence in machines.
It enables machines to learn, reason, solve problems, and make decisions.
"""

response = """
Artificial Intelligence is the simulation of human intelligence in machines.
"""

result = evaluate_completeness(question, response, reference)

print(result)
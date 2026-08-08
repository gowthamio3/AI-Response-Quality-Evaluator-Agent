from llm import ask_llm

def evaluate_relevance(question, response):
    prompt = f"""
You are a Relevance Judge Agent.

Question:
{question}

AI Response:
{response}

Evaluate how relevant the response is to the question.

Return only in this format:

Relevance Score: X/10
Reason: <one or two sentences>
"""

    result = ask_llm(prompt)
    return result
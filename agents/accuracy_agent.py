from llm import ask_llm

def evaluate_accuracy(question, response, reference):
    prompt = f"""
You are an Accuracy Judge Agent.

Question:
{question}

Reference Answer:
{reference}

AI Response:
{response}

Compare the AI response with the reference answer.

Return only in this format:

Accuracy Score: X/10
Reason: <one or two sentences>
"""

    return ask_llm(prompt)
from llm import ask_llm

def detect_hallucination(question, response, reference):
    prompt = f"""
You are a Hallucination Detection Agent.

Question:
{question}

Reference Answer:
{reference}

AI Response:
{response}

Check whether the AI response contains information that is NOT supported by the reference answer.

Return only in this format:

Hallucination Score: X/10
Reason: <one or two sentences>
"""
    return ask_llm(prompt)
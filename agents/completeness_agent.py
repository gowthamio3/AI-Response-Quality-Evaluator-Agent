from llm import ask_llm

def evaluate_completeness(question, response, reference):
    prompt = f"""
You are a Completeness Judge Agent.

Question:
{question}

Reference Answer:
{reference}

AI Response:
{response}

Evaluate whether the AI response covers all the important aspects of the question by comparing it with the reference answer.

Identify any missing information.

Return only in this format:

Completeness Score: X/10
Reason: <one or two sentences>
Missing Points:
- <missing point 1>
- <missing point 2>

If nothing is missing, write:

Missing Points:
None
"""

    return ask_llm(prompt)
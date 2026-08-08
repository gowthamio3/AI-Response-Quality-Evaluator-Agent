from llm import ask_llm

def evaluate_verdict(
    relevance,
    accuracy,
    completeness,
    hallucination
):
    prompt = f"""
You are a Verdict Agent.

You are given the evaluation results from four judge agents.

Relevance Evaluation:
{relevance}

Accuracy Evaluation:
{accuracy}

Completeness Evaluation:
{completeness}

Hallucination Evaluation:
{hallucination}

Based on these evaluations:

1. Calculate an Overall Score out of 10 using a weighted scoring model.
2. Give one Final Verdict:
   - PASS
   - NEEDS IMPROVEMENT
   - FAIL
3. Provide a short Consolidated Reasoning.

Return only in this format:

Overall Score: X/10
Final Verdict: PASS / NEEDS IMPROVEMENT / FAIL
Consolidated Reasoning:
<two or three sentences>
"""

    return ask_llm(prompt)
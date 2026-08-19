import re


def extract_score(text, score_name):
    """
    Extract a score out of 10 from an agent's response.

    Example:
    'Accuracy Score: 8/10'
    returns:
    8.0
    """

    if not text:
        return None

    pattern = rf"{re.escape(score_name)}\s*Score:\s*(\d+(?:\.\d+)?)\s*/\s*10"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1))

    return None


def extract_verdict(text):
    """
    Extract the final verdict from the Verdict Agent response.

    Returns:
    PASS
    NEEDS IMPROVEMENT
    FAIL
    """

    if not text:
        return None

    pattern = r"Final Verdict:\s*(PASS|NEEDS IMPROVEMENT|FAIL)"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group(1).upper()

    return None


def extract_overall_score(text):
    """
    Extract the overall score from the Verdict Agent response.

    Example:
    'Overall Score: 8/10'
    returns:
    8.0
    """

    if not text:
        return None

    pattern = r"Overall Score:\s*(\d+(?:\.\d+)?)\s*/\s*10"

    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1))

    return None
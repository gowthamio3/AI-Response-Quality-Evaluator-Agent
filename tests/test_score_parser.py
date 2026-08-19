from score_parser import (
    extract_score,
    extract_verdict,
    extract_overall_score
)


def test_score_parser():

    accuracy_result = """
    Accuracy Score: 8/10
    Reason: The response is mostly correct.
    """

    relevance_result = """
    Relevance Score: 9/10
    Reason: The response directly addresses the question.
    """

    verdict_result = """
    Overall Score: 8/10
    Final Verdict: PASS
    Consolidated Reasoning:
    The response is accurate and relevant.
    """

    accuracy = extract_score(
        accuracy_result,
        "Accuracy"
    )

    relevance = extract_score(
        relevance_result,
        "Relevance"
    )

    overall = extract_overall_score(
        verdict_result
    )

    verdict = extract_verdict(
        verdict_result
    )

    print("Accuracy:", accuracy)
    print("Relevance:", relevance)
    print("Overall:", overall)
    print("Verdict:", verdict)

    assert accuracy == 8.0
    assert relevance == 9.0
    assert overall == 8.0
    assert verdict == "PASS"


if __name__ == "__main__":
    test_score_parser()
    print("✅ Score parser test passed!")
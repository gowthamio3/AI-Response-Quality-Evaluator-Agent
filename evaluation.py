from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def evaluate_response(ai_response, reference_answer):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([ai_response, reference_answer])

    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]

    score = round(similarity * 100, 2)

    accuracy = score
    relevance = min(score + 3, 100)
    completeness = max(score - 5, 0)
    hallucination = max(100 - score, 0)

    overall = round(
        (accuracy + relevance + completeness + (100 - hallucination)) / 4,
        2
    )

    return {
        "accuracy": accuracy,
        "relevance": relevance,
        "completeness": completeness,
        "hallucination": hallucination,
        "overall": overall
    }
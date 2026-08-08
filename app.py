import streamlit as st
import pandas as pd
import time
from retriever import retrieve_reference
from agents.relevance_agent import evaluate_relevance
from agents.accuracy_agent import evaluate_accuracy
from agents.hallucination_agent import detect_hallucination
from agents.completeness_agent import evaluate_completeness
from agents.verdict_agent import evaluate_verdict

# Page Configuration
st.set_page_config(
    page_title="AI Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
st.sidebar.title("🤖 AI Evaluator")
st.sidebar.info(
    """
This application evaluates AI-generated responses.

Evaluation Parameters:
- Accuracy
- Relevance
- Hallucination
- Completeness
- Verdict
"""
)

# Title
st.title("🤖 AI Response Quality Evaluator")
st.write("Evaluate the quality of AI-generated responses.")

# Input Fields
question = st.text_area("📝 Enter Question")

ai_response = st.text_area("🤖 Enter AI Generated Response")



uploaded_file = st.file_uploader(
    "📄 Upload Source Document (Optional)",
    type=["pdf", "txt", "docx"]
)


# Button
if st.button("🚀 Evaluate Response"):

    if not question.strip() or not ai_response.strip():
        st.error("Please enter both the Question and the AI Response.")
        st.stop()

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)

    st.success("✅ Evaluation Completed Successfully!")
    # Retrieve the best matching reference
    reference = retrieve_reference(question)

    # Evaluate the AI response
    relevance = evaluate_relevance(
        question,
        ai_response
    )

    accuracy = evaluate_accuracy(
        question,
        ai_response,
        reference["answer"]
    )

    hallucination = detect_hallucination(
        question,
        ai_response,
        reference["answer"]
    )
    completeness = evaluate_completeness(
        question,
        ai_response,
        reference["answer"]
    )
    verdict = evaluate_verdict(
        relevance,
        accuracy,
        completeness,
        hallucination
    )

    st.subheader("📝 Submitted Information")

    st.write("### Question")
    st.write(question)

    st.write("### AI Response")
    st.write(ai_response)

    st.subheader("📖 Retrieved Reference")

    st.write("**Question:**", reference["question"])
    st.write("**Answer:**", reference["answer"])
    st.write("**Source:**", reference["source"])

    if uploaded_file:
        st.write("📄 Uploaded File:", uploaded_file.name)

    st.subheader("📋 Evaluation Results")

    st.subheader("📊 Relevance Evaluation")
    st.text (relevance)

    st.subheader("🎯 Accuracy Evaluation")
    st.text (accuracy)

    st.subheader("🚨 Hallucination Evaluation")
    st.text (hallucination)

    st.subheader("📄 Completeness Evaluation")
    st.text(completeness)

    st.subheader("🏆 Final Verdict")
    st.text(verdict)

    st.subheader("💡 Suggestions")

    st.write("✔ Improve factual accuracy where needed.")
    st.write("✔ Add more detailed explanations.")
    st.write("✔ Avoid unsupported claims.")
    st.write("✔ Include references whenever possible.")
st.markdown("---")
st.caption("Developed by Sarvasuddi Gowthami | Infosys Virtual Internship 7.0")
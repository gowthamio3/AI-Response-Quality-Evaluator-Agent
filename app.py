import streamlit as st
import pandas as pd
import time

from retriever import retrieve_reference
from score_parser import (
    extract_score,
    extract_verdict,
    extract_overall_score
)

from agents.relevance_agent import evaluate_relevance
from agents.accuracy_agent import evaluate_accuracy
from agents.hallucination_agent import detect_hallucination
from agents.completeness_agent import evaluate_completeness
from agents.verdict_agent import evaluate_verdict

from batch_module import show_batch_evaluation
from dashboard_module import show_dashboard


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Development of AI Response Validation System with Hallucination Detection Assistance Group1",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🤖 AI Evaluator")

page = st.sidebar.radio(
    "Select Module",
    [
        "📝 Single Evaluation",
        "📂 Batch Evaluation",
        "📊 Dashboard"
    ]
)

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


# ============================================================
# BATCH EVALUATION
# ============================================================

if page == "📂 Batch Evaluation":

    show_batch_evaluation()


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    show_dashboard()


# ============================================================
# SINGLE EVALUATION
# ============================================================

else:

    # ========================================================
    # TITLE
    # ========================================================

    st.title(
        "🤖 Development of AI Response Validation System "
        "with Hallucination Detection Assistance Group1"
    )

    st.write(
        "Evaluate the quality of AI-generated responses."
    )


    # ========================================================
    # STORED AI RESPONSES
    # ========================================================
    # These are the responses collected from Copilot and Gemini.
    # Add more questions/responses here later if required.

    AI_RESPONSES = {

        "what is artificial intelligence": {

            "Copilot": """Artificial intelligence (AI) is the science and engineering of creating computer systems that can perform tasks requiring human-like intelligence, such as learning, reasoning, problem-solving, and decision-making. In simple terms, it’s about teaching machines to “think” and act intelligently.""",

            "Gemini": """Artificial Intelligence (AI) is a field of computer science dedicated to building systems capable of performing tasks that typically require human intelligence.

Rather than relying purely on explicit, line-by-line programming, modern AI systems learn patterns from data to reason, generalize, and make decisions."""
        },

        "what is machine learning": {

            "Copilot": """Machine learning (ML) is a branch of artificial intelligence that enables computers to learn from data, identify patterns, and make decisions or predictions without being explicitly programmed. In essence, it’s about teaching machines to improve their performance automatically through experience.""",

            "Gemini": """Machine Learning (ML) is a subfield of Artificial Intelligence (AI) focused on building algorithms that allow computers to learn from data and improve their performance over time without being explicitly programmed."""
        },

        "what is retrieval-augmented generation": {

            "Copilot": """Retrieval-Augmented Generation (RAG) is an AI technique that combines large language models (LLMs) with external knowledge sources to produce more accurate, up-to-date, and context-specific responses. Instead of relying only on static training data, RAG retrieves relevant documents at query time and feeds them into the model, grounding its answers in real-world information.""",

            "Gemini": """Retrieval-Augmented Generation (RAG) is an AI framework that connects a large language model (LLM) to external knowledge sources—such as databases, internal documents, or the web—before generating a response. Standard LLMs rely entirely on the static knowledge learned during their pre-training. RAG improves this by retrieving relevant, real-time facts from a curated dataset and supplying them alongside your prompt as context."""
        },

        "what is hallucination in ai": {

            "Copilot": """In large language models (LLMs), a “hallucination” refers to the generation of text that is fluent and convincing but factually incorrect, unsupported by evidence, or unrelated to the input. It’s one of the biggest challenges in AI because the output sounds right but may mislead users.""",

            "Gemini": """In Large Language Models (LLMs), a hallucination occurs when a model generates text that sounds fluent, plausible, and confident, but is factually incorrect, logically inconsistent, or completely fabricated."""
        },

        "why is ai evaluation important": {

            "Copilot": """AI evaluation is crucial because it ensures that artificial intelligence systems are trustworthy, effective, and safe. Without proper evaluation, we risk deploying models that are biased, unreliable, or even harmful. Let me break it down.""",

            "Gemini": """AI evaluation is the systematic process of assessing an AI model’s performance, reliability, safety, and alignment before and after deployment. Because AI systems—especially Generative AI—behave non-deterministically, continuous evaluation acts as the primary quality control mechanism."""
        }
    }


    # ========================================================
    # EVALUATION FUNCTION
    # ========================================================

    def evaluate_ai_response(question, ai_response, reference):

        relevance = evaluate_relevance(
            question,
            ai_response
        )

        accuracy = evaluate_accuracy(
            question,
            ai_response,
            reference
        )

        hallucination = detect_hallucination(
            question,
            ai_response,
            reference
        )

        completeness = evaluate_completeness(
            question,
            ai_response,
            reference
        )

        verdict = evaluate_verdict(
            relevance,
            accuracy,
            completeness,
            hallucination
        )

        return {
            "response": ai_response,
            "relevance": relevance,
            "accuracy": accuracy,
            "hallucination": hallucination,
            "completeness": completeness,
            "verdict": verdict
        }


    # ========================================================
    # INITIAL SINGLE EVALUATION
    # ========================================================

    question = st.text_area(
        "📝 Enter Question"
    )

    ai_response = st.text_area(
        "🤖 Enter AI Generated Response"
    )

    uploaded_file = st.file_uploader(
        "📄 Upload Source Document (Optional)",
        type=["pdf", "txt", "docx"]
    )


    # ========================================================
    # EVALUATE BUTTON
    # ========================================================

    if st.button(
        "🚀 Evaluate Response",
        key="single_evaluate_button"
    ):

        if not question.strip() or not ai_response.strip():

            st.error(
                "Please enter both the Question and the AI Response."
            )

            st.stop()

        progress = st.progress(0)

        for i in range(100):

            time.sleep(0.01)

            progress.progress(i + 1)

        reference = retrieve_reference(
            question
        )

        result = evaluate_ai_response(
            question,
            ai_response,
            reference["answer"]
        )

        # Store initial evaluation
        st.session_state["single_evaluation_done"] = True
        st.session_state["question"] = question
        st.session_state["reference"] = reference
        st.session_state["initial_result"] = result

        # Reset comparison
        st.session_state["copilot_result"] = None
        st.session_state["gemini_result"] = None

        st.success(
            "✅ Evaluation Completed Successfully!"
        )


    # ========================================================
    # DISPLAY INITIAL SINGLE EVALUATION
    # ========================================================

    if st.session_state.get(
        "single_evaluation_done",
        False
    ):

        question = st.session_state[
            "question"
        ]

        reference = st.session_state[
            "reference"
        ]

        result = st.session_state[
            "initial_result"
        ]

        st.subheader(
            "📝 Submitted Information"
        )

        st.write(
            "### Question"
        )

        st.write(
            question
        )

        st.write(
            "### AI Response"
        )

        st.write(
            result["response"]
        )


        # ----------------------------------------------------
        # REFERENCE
        # ----------------------------------------------------

        st.subheader(
            "📖 Retrieved Reference"
        )

        st.write(
            "**Question:**",
            reference["question"]
        )

        st.write(
            "**Answer:**",
            reference["answer"]
        )

        st.write(
            "**Source:**",
            reference["source"]
        )

        if uploaded_file:

            st.write(
                "📄 Uploaded File:",
                uploaded_file.name
            )


        # ----------------------------------------------------
        # SINGLE EVALUATION RESULTS
        # ----------------------------------------------------

        st.subheader(
            "📋 Evaluation Results"
        )

        st.subheader(
            "📊 Relevance Evaluation"
        )

        st.text(
            result["relevance"]
        )

        st.subheader(
            "🎯 Accuracy Evaluation"
        )

        st.text(
            result["accuracy"]
        )

        st.subheader(
            "🚨 Hallucination Evaluation"
        )

        st.text(
            result["hallucination"]
        )

        st.subheader(
            "📄 Completeness Evaluation"
        )

        st.text(
            result["completeness"]
        )

        st.subheader(
            "🏆 Final Verdict"
        )

        st.text(
            result["verdict"]
        )


        # ====================================================
        # TWO AI RESPONSES
        # ====================================================

        normalized_question = (
            question.strip().lower()
        )

        if normalized_question in AI_RESPONSES:

            st.divider()

            st.header(
                "🤖 Compare Two AI Systems"
            )

            st.write(
                "Select an AI system to automatically evaluate "
                "its response using the same question and "
                "reference answer."
            )

            col1, col2 = st.columns(2)


            # ------------------------------------------------
            # COPILOT
            # ------------------------------------------------

            with col1:

                if st.button(
                    "🟦 Evaluate Copilot",
                    use_container_width=True,
                    key="evaluate_copilot_button"
                ):

                    copilot_response = AI_RESPONSES[
                        normalized_question
                    ]["Copilot"]

                    with st.spinner(
                        "Evaluating Copilot response..."
                    ):

                        st.session_state[
                            "copilot_result"
                        ] = evaluate_ai_response(
                            question,
                            copilot_response,
                            reference["answer"]
                        )


            # ------------------------------------------------
            # GEMINI
            # ------------------------------------------------

            with col2:

                if st.button(
                    "🟩 Evaluate Gemini",
                    use_container_width=True,
                    key="evaluate_gemini_button"
                ):

                    gemini_response = AI_RESPONSES[
                        normalized_question
                    ]["Gemini"]

                    with st.spinner(
                        "Evaluating Gemini response..."
                    ):

                        st.session_state[
                            "gemini_result"
                        ] = evaluate_ai_response(
                            question,
                            gemini_response,
                            reference["answer"]
                        )


            # =================================================
            # DISPLAY COPILOT
            # =================================================

            if st.session_state.get(
                "copilot_result"
            ):

                copilot = st.session_state[
                    "copilot_result"
                ]

                st.divider()

                st.subheader(
                    "🟦 Copilot Evaluation"
                )

                st.write(
                    "### 🤖 Copilot Response"
                )

                st.write(
                    copilot["response"]
                )

                st.write(
                    "### 📊 Evaluation"
                )

                st.text(
                    copilot["relevance"]
                )

                st.text(
                    copilot["accuracy"]
                )

                st.text(
                    copilot["hallucination"]
                )

                st.text(
                    copilot["completeness"]
                )

                st.write(
                    "### 🏆 Verdict"
                )

                st.text(
                    copilot["verdict"]
                )


            # =================================================
            # DISPLAY GEMINI
            # =================================================

            if st.session_state.get(
                "gemini_result"
            ):

                gemini = st.session_state[
                    "gemini_result"
                ]

                st.divider()

                st.subheader(
                    "🟩 Gemini Evaluation"
                )

                st.write(
                    "### 🤖 Gemini Response"
                )

                st.write(
                    gemini["response"]
                )

                st.write(
                    "### 📊 Evaluation"
                )

                st.text(
                    gemini["relevance"]
                )

                st.text(
                    gemini["accuracy"]
                )

                st.text(
                    gemini["hallucination"]
                )

                st.text(
                    gemini["completeness"]
                )

                st.write(
                    "### 🏆 Verdict"
                )

                st.text(
                    gemini["verdict"]
                )


            # =================================================
            # COMPARISON
            # =================================================

            if (
                st.session_state.get(
                    "copilot_result"
                )
                and
                st.session_state.get(
                    "gemini_result"
                )
            ):

                st.divider()

                st.header(
                    "📊 Copilot vs Gemini Comparison"
                )

                copilot = st.session_state[
                    "copilot_result"
                ]

                gemini = st.session_state[
                    "gemini_result"
                ]


                copilot_relevance = extract_score(
                    copilot["relevance"],
                    "Relevance"
                )

                gemini_relevance = extract_score(
                    gemini["relevance"],
                    "Relevance"
                )


                copilot_accuracy = extract_score(
                    copilot["accuracy"],
                    "Accuracy"
                )

                gemini_accuracy = extract_score(
                    gemini["accuracy"],
                    "Accuracy"
                )


                copilot_hallucination = extract_score(
                    copilot["hallucination"],
                    "Hallucination"
                )

                gemini_hallucination = extract_score(
                    gemini["hallucination"],
                    "Hallucination"
                )


                copilot_completeness = extract_score(
                    copilot["completeness"],
                    "Completeness"
                )

                gemini_completeness = extract_score(
                    gemini["completeness"],
                    "Completeness"
                )


                copilot_overall = extract_overall_score(
                    copilot["verdict"]
                )

                gemini_overall = extract_overall_score(
                    gemini["verdict"]
                )


                copilot_verdict = extract_verdict(
                    copilot["verdict"]
                )

                gemini_verdict = extract_verdict(
                    gemini["verdict"]
                )


                comparison_df = pd.DataFrame({

                    "Metric": [
                        "Relevance",
                        "Accuracy",
                        "Hallucination",
                        "Completeness",
                        "Overall Score",
                        "Final Verdict"
                    ],

                    "🟦 Copilot": [
                        copilot_relevance,
                        copilot_accuracy,
                        copilot_hallucination,
                        copilot_completeness,
                        copilot_overall,
                        copilot_verdict
                    ],

                    "🟩 Gemini": [
                        gemini_relevance,
                        gemini_accuracy,
                        gemini_hallucination,
                        gemini_completeness,
                        gemini_overall,
                        gemini_verdict
                    ]
                })


                st.dataframe(
                    comparison_df,
                    use_container_width=True,
                    hide_index=True
                )


                st.success(
                    "✅ Both AI systems have been evaluated "
                    "using the same question and reference answer."
                )

        else:

            st.warning(
                "⚠️ Two-AI comparison is currently available "
                "for the questions stored in the comparison dataset."
            )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("---")

    st.caption(
        "Developed by Sarvasuddi Gowthami | "
        "Infosys Virtual Internship 7.0"
    )
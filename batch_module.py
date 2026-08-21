import streamlit as st
import pandas as pd

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


def show_batch_evaluation():

    st.title("📊 Batch Evaluation Module")

    st.write(
        "Upload a CSV containing **Question**, "
        "**AI_Response**, and **Reference Answer**."
    )

    csv_file = st.file_uploader(
        "📂 Upload CSV File",
        type=["csv"],
        key="batch_csv_uploader"
    )

    if csv_file is not None:

        df = pd.read_csv(csv_file)

        st.subheader("📄 Uploaded CSV")
        st.dataframe(df, use_container_width=True)

        required_columns = [
            "Question",
            "AI_Response",
            "Reference Answer"
        ]

        if not all(col in df.columns for col in required_columns):

            st.error(
                "CSV must contain these columns:\n\n"
                "• Question\n"
                "• AI_Response\n"
                "• Reference Answer"
            )

        else:

            if st.button(
                "🚀 Start Batch Evaluation",
                key="start_batch_evaluation"
            ):

                results = []

                progress = st.progress(0)

                total_rows = len(df)

                for i, row in df.iterrows():

                    question = row["Question"]
                    ai_response = row["AI_Response"]
                    reference = row["Reference Answer"]

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

                    relevance_score = extract_score(
                        relevance,
                        "Relevance"
                    )

                    accuracy_score = extract_score(
                        accuracy,
                        "Accuracy"
                    )

                    hallucination_score = extract_score(
                        hallucination,
                        "Hallucination"
                    )

                    completeness_score = extract_score(
                        completeness,
                        "Completeness"
                    )

                    overall_score = extract_overall_score(
                        verdict
                    )

                    final_verdict = extract_verdict(
                        verdict
                    )

                    results.append({

                        "Question": question,
                        "AI Response": ai_response,

                        "Relevance": relevance_score,
                        "Accuracy": accuracy_score,
                        "Hallucination": hallucination_score,
                        "Completeness": completeness_score,

                        "Overall Score": overall_score,
                        "Verdict": final_verdict,

                        "Relevance Details": relevance,
                        "Accuracy Details": accuracy,
                        "Hallucination Details": hallucination,
                        "Completeness Details": completeness,
                        "Verdict Details": verdict
                    })

                    progress.progress(
                        int((i + 1) * 100 / total_rows)
                    )

                result_df = pd.DataFrame(results)

                # Store results for Dashboard
                st.session_state[
                    "evaluation_results"
                ] = result_df

                st.success(
                    f"✅ Successfully evaluated "
                    f"{len(results)} responses."
                )

    # Display existing batch results
    if "evaluation_results" in st.session_state:

        result_df = st.session_state[
            "evaluation_results"
        ]

        display_df = result_df[
            [
                "Question",
                "Relevance",
                "Accuracy",
                "Hallucination",
                "Completeness",
                "Overall Score",
                "Verdict"
            ]
        ]

        st.divider()

        st.subheader("📊 Batch Summary")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Total Responses",
                len(result_df)
            )

        with col2:
            st.metric(
                "Completed",
                len(result_df)
            )

        st.divider()

        st.subheader("📋 Batch Evaluation Results")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        csv = display_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Evaluation Report",
            data=csv,
            file_name="batch_evaluation_results.csv",
            mime="text/csv",
            key="download_batch_results"
        )
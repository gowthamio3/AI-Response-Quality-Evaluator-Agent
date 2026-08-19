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

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Batch Evaluation Module",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Batch Evaluation Module")
st.write(
    "Upload a CSV containing **Question**, **AI_Response**, and **Reference Answer**."
)

# ---------------------------------------------------
# Upload CSV
# ---------------------------------------------------

csv_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

# ---------------------------------------------------
# Batch Evaluation
# ---------------------------------------------------

if csv_file is not None:

    df = pd.read_csv(csv_file)


    st.subheader("📄 Uploaded CSV")
    st.dataframe(df, use_container_width=True)

    required_columns = [
        "Question",
        "AI_Response",
        "Reference Answer",

    ]

    if not all(col in df.columns for col in required_columns):

        st.error(
            "CSV must contain these columns:\n\n"
            "• Question\n"
            "• AI_Response\n"
            "• Reference Answer"
        )

    else:

        if st.button("🚀 Start Batch Evaluation"):

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

                # ---------------------------------------------------
                # Extract Structured Scores
                # ---------------------------------------------------

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

                # ---------------------------------------------------
                # Store Structured Evaluation Result
                # ---------------------------------------------------

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

                progress.progress(int((i + 1) * 100 / total_rows))

            st.success(f"✅ Successfully evaluated {len(results)} responses.")

            result_df = pd.DataFrame(results)
            # Save structured results for Milestone 4 Dashboard
            result_df.to_csv(
                "evaluation_results.csv",
                index=False
            )

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

            # ---------------------------------------------------
            # Summary
            # ---------------------------------------------------

            st.subheader("📊 Batch Summary")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Total Responses", len(results))

            with col2:
                st.metric("Completed", len(results))

            st.divider()

            # ---------------------------------------------------
            # Results Table
            # ---------------------------------------------------

            st.subheader("📋 Batch Evaluation Results")

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            st.divider()

            # ---------------------------------------------------
            # Detailed Evaluation
            # ---------------------------------------------------

            st.subheader("📄 Detailed Analysis")

            for i, row in enumerate(results):

                with st.expander(f"📌 Question {i + 1}: {row['Question']}"):

                    st.write("### 🤖 AI Response")
                    st.write(row["AI Response"])

                    # ---------------------------------------------------
                    # Relevance
                    # ---------------------------------------------------

                    st.write("### 🎯 Relevance")

                    relevance_score = extract_score(
                        row["Relevance Details"],
                        "Relevance"
                    )

                    relevance_reason = row["Relevance Details"].split(
                        "Reason:", 1
                    )[-1].strip()

                    st.write(f"**Score:** {relevance_score}/10")
                    st.write(f"**Reason:** {relevance_reason}")

                    # ---------------------------------------------------
                    # Accuracy
                    # ---------------------------------------------------

                    st.write("### 🎯 Accuracy")

                    accuracy_score = extract_score(
                        row["Accuracy Details"],
                        "Accuracy"
                    )

                    accuracy_reason = row["Accuracy Details"].split(
                        "Reason:", 1
                    )[-1].strip()

                    st.write(f"**Score:** {accuracy_score}/10")
                    st.write(f"**Reason:** {accuracy_reason}")

                    # ---------------------------------------------------
                    # Hallucination
                    # ---------------------------------------------------

                    st.write("### 🚨 Hallucination")

                    hallucination_score = extract_score(
                        row["Hallucination Details"],
                        "Hallucination"
                    )

                    hallucination_reason = row["Hallucination Details"].split(
                        "Reason:", 1
                    )[-1].strip()

                    st.write(f"**Score:** {hallucination_score}/10")
                    st.write(f"**Reason:** {hallucination_reason}")

                    # ---------------------------------------------------
                    # Completeness
                    # ---------------------------------------------------

                    st.write("### 📄 Completeness")

                    completeness_score = extract_score(
                        row["Completeness Details"],
                        "Completeness"
                    )

                    completeness_reason = row["Completeness Details"].split(
                        "Reason:", 1
                    )[1].split("Missing Points:", 1)[0].strip()

                    st.write(f"**Score:** {completeness_score}/10")
                    st.write(f"**Reason:** {completeness_reason}")

                    # ---------------------------------------------------
                    # Overall Score
                    # ---------------------------------------------------

                    st.write("### 🏆 Overall Score")
                    st.write(f"**{row['Overall Score']}/10**")

                    # ---------------------------------------------------
                    # Verdict
                    # ---------------------------------------------------

                    st.write("### 🏆 Verdict")
                    st.write(f"**{row['Verdict']}**")

                    # ---------------------------------------------------
                    # Verdict Details
                    # ---------------------------------------------------

                    st.write("### 📝 Verdict Details")

                    verdict_details = row["Verdict Details"]

                    if "Consolidated Reasoning:" in verdict_details:

                        reasoning = verdict_details.split(
                            "Consolidated Reasoning:", 1
                        )[1].strip()

                        st.write(f"**Reason:** {reasoning}")

                    else:
                        st.write(verdict_details)
            st.divider()

            # ---------------------------------------------------
            # Download Button
            # ---------------------------------------------------

            csv = display_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Evaluation Report",
                data=csv,
                file_name="batch_evaluation_results.csv",
                mime="text/csv"
            )

st.markdown("---")
st.caption("Developed by Sarvasuddi Gowthami | Infosys Virtual Internship 7.0")
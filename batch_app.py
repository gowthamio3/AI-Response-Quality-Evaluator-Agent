import streamlit as st
import pandas as pd

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

                results.append({

                    "Question": question,
                    "AI Response": ai_response,

                    "Relevance": relevance.split("Reason")[0].replace("Score:", "").strip(),
                    "Accuracy": accuracy.split("Reason")[0].replace("Score:", "").strip(),
                    "Hallucination": hallucination.split("Reason")[0].replace("Score:", "").strip(),
                    "Completeness": completeness.split("Reason")[0].replace("Score:", "").strip(),
                    "Verdict": verdict,

                    "Relevance Details": relevance,
                    "Accuracy Details": accuracy,
                    "Hallucination Details": hallucination,
                    "Completeness Details": completeness

                })

                progress.progress(int((i + 1) * 100 / total_rows))

            st.success(f"✅ Successfully evaluated {len(results)} responses.")

            result_df = pd.DataFrame(results)

            display_df = result_df[
                [
                    "Question",
                    "Relevance",
                    "Accuracy",
                    "Hallucination",
                    "Completeness",
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

                with st.expander(f"📌 Question {i+1}: {row['Question']}"):

                    st.write("### 🤖 AI Response")
                    st.write(row["AI Response"])

                    st.write("### 🎯 Relevance")
                    st.write(row["Relevance Details"])

                    st.write("### 🎯 Accuracy")
                    st.write(row["Accuracy Details"])

                    st.write("### 🚨 Hallucination")
                    st.write(row["Hallucination Details"])

                    st.write("### 📄 Completeness")
                    st.write(row["Completeness Details"])

                    st.write("### 🏆 Verdict")
                    st.write(row["Verdict"])

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
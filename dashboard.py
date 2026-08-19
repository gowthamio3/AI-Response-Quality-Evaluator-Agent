import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="AI Response Validation Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Response Validation Dashboard")

st.caption(
    "Analyze the quality, accuracy and reliability of AI-generated responses."
)


# =====================================================
# LOAD DATA
# =====================================================

try:
    df = pd.read_csv("evaluation_results.csv")

except FileNotFoundError:
    st.error("evaluation_results.csv not found.")
    st.stop()


# =====================================================
# CLEAN DATA
# =====================================================

score_columns = [
    "Relevance",
    "Accuracy",
    "Hallucination",
    "Completeness",
    "Overall Score"
]

for column in score_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df["Verdict"] = (
    df["Verdict"]
    .astype(str)
    .str.upper()
    .str.strip()
)

df = df.dropna(subset=score_columns)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🎛️ Dashboard")

selected_verdict = st.sidebar.selectbox(
    "Filter by Verdict",
    [
        "ALL",
        "PASS",
        "NEEDS IMPROVEMENT",
        "FAIL"
    ]
)

if selected_verdict == "ALL":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["Verdict"] == selected_verdict
    ].copy()


# =====================================================
# CALCULATIONS
# =====================================================

total = len(filtered_df)

pass_count = (
    filtered_df["Verdict"] == "PASS"
).sum()

needs_count = (
    filtered_df["Verdict"] == "NEEDS IMPROVEMENT"
).sum()

fail_count = (
    filtered_df["Verdict"] == "FAIL"
).sum()


if total > 0:

    average_score = filtered_df[
        "Overall Score"
    ].mean()

    relevance = filtered_df[
        "Relevance"
    ].mean()

    accuracy = filtered_df[
        "Accuracy"
    ].mean()

    completeness = filtered_df[
        "Completeness"
    ].mean()

else:

    average_score = 0
    relevance = 0
    accuracy = 0
    completeness = 0


hallucinated = (
    filtered_df["Hallucination"] >= 5
).sum()

hallucination_rate = (
    hallucinated / total * 100
    if total > 0
    else 0
)


# =====================================================
# SUMMARY
# =====================================================

st.subheader("📊 Evaluation Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Evaluations",
        total
    )

with c2:
    st.metric(
        "Average Score",
        f"{average_score:.2f}/10"
    )

with c3:
    st.metric(
        "PASS",
        pass_count
    )

with c4:
    st.metric(
        "Issues Detected",
        needs_count + fail_count
    )


st.divider()


# =====================================================
# QUALITY DIMENSIONS
# =====================================================

st.subheader("🎯 Quality Dimensions")

q1, q2, q3 = st.columns(3)

with q1:

    st.write("**Relevance**")

    st.progress(
        int(relevance * 10)
    )

    st.caption(
        f"{relevance:.2f} / 10"
    )


with q2:

    st.write("**Accuracy**")

    st.progress(
        int(accuracy * 10)
    )

    st.caption(
        f"{accuracy:.2f} / 10"
    )


with q3:

    st.write("**Completeness**")

    st.progress(
        int(completeness * 10)
    )

    st.caption(
        f"{completeness:.2f} / 10"
    )


st.divider()


# =====================================================
# VERDICT + HALLUCINATION
# =====================================================

left, right = st.columns(2)


# -----------------------------------------------------
# VERDICT
# -----------------------------------------------------

with left:

    st.subheader("🏆 Verdict Distribution")

    verdict_data = pd.DataFrame({
        "Verdict": [
            "PASS",
            "NEEDS IMPROVEMENT",
            "FAIL"
        ],
        "Count": [
            pass_count,
            needs_count,
            fail_count
        ]
    })

    st.bar_chart(
        verdict_data.set_index("Verdict")
    )

    st.caption(
        f"Total evaluated: {total}"
    )


# -----------------------------------------------------
# HALLUCINATION
# -----------------------------------------------------

with right:

    st.subheader("🚨 Hallucination Analysis")

    st.metric(
        "Hallucination Frequency",
        f"{hallucination_rate:.1f}%"
    )

    if hallucinated > 0:

        st.warning(
            f"{hallucinated} of {total} "
            "responses have significant "
            "hallucination risk."
        )

    else:

        st.success(
            "No significant hallucination "
            "issues detected."
        )


st.divider()


# =====================================================
# RESPONSE SCORE COMPARISON
# =====================================================

st.subheader("📈 Response Score Comparison")

if total > 0:

    chart_df = filtered_df[
        ["Overall Score"]
    ].copy()

    chart_df.index = [
        f"Response {i + 1}"
        for i in range(len(chart_df))
    ]

    st.bar_chart(
        chart_df,
        y="Overall Score"
    )

    st.caption(
        "Overall score comparison for each evaluated response."
    )

else:

    st.info(
        "No responses available for comparison."
    )


st.divider()


# =====================================================
# DIMENSION COMPARISON
# =====================================================

st.subheader("📊 Dimension Score Comparison")

if total > 0:

    dimension_df = filtered_df[
        [
            "Relevance",
            "Accuracy",
            "Hallucination",
            "Completeness"
        ]
    ].copy()

    dimension_df.index = [
        f"Response {i + 1}"
        for i in range(len(dimension_df))
    ]

    st.line_chart(
        dimension_df
    )

else:

    st.info(
        "No dimension data available."
    )


st.divider()


# =====================================================
# DETAILED RESULTS
# =====================================================

st.subheader("📋 Detailed Evaluation Results")

if total == 0:

    st.info(
        "No evaluations match the selected filter."
    )

else:

    for i, (_, row) in enumerate(
        filtered_df.iterrows()
    ):

        with st.expander(
            f"Response {i + 1} — {row['Verdict']}"
        ):

            st.markdown(
                f"### Question"
            )

            st.write(
                row["Question"]
            )

            st.markdown(
                "### 🤖 AI Response"
            )

            st.write(
                row["AI Response"]
            )

            st.markdown(
                "### 🎯 Evaluation Scores"
            )

            s1, s2, s3, s4, s5 = st.columns(5)

            with s1:
                st.metric(
                    "Relevance",
                    f"{row['Relevance']:.1f}/10"
                )

            with s2:
                st.metric(
                    "Accuracy",
                    f"{row['Accuracy']:.1f}/10"
                )

            with s3:
                st.metric(
                    "Hallucination",
                    f"{row['Hallucination']:.1f}/10"
                )

            with s4:
                st.metric(
                    "Completeness",
                    f"{row['Completeness']:.1f}/10"
                )

            with s5:
                st.metric(
                    "Overall",
                    f"{row['Overall Score']:.1f}/10"
                )

            st.markdown(
                f"### 🏆 Final Verdict: **{row['Verdict']}**"
            )


st.divider()


# =====================================================
# RESULTS TABLE
# =====================================================

st.subheader("📄 Evaluation Summary Table")

display_columns = [
    "Question",
    "Relevance",
    "Accuracy",
    "Hallucination",
    "Completeness",
    "Overall Score",
    "Verdict"
]

st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)


# =====================================================
# DOWNLOAD
# =====================================================

st.divider()

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Evaluation Results",
    csv_data,
    "evaluation_results.csv",
    "text/csv"
)


# =====================================================
# FOOTER
# =====================================================

st.caption(
    "Development of AI Response Validation System with "
    "Hallucination Detection Assistance | "
    "Infosys Virtual Internship 7.0"
)
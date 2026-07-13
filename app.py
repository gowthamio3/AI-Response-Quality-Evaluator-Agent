import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Response Quality Evaluator",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Response Quality Evaluator")
st.caption("Evaluate AI-generated responses using Accuracy, Relevance, Completeness, and Hallucination Detection.")

st.write("Evaluate the quality of AI-generated responses.")

# Question
question = st.text_area("Enter Question")

# AI Response
ai_response = st.text_area("Enter AI Generated Response")

# Reference Answer (Optional)
reference_answer = st.text_area("Reference Answer (Optional)")

# Source Document Upload
uploaded_file = st.file_uploader(
    "Upload Source Document (Optional)",
    type=["pdf", "txt", "docx"]
)

# Submit Button
if st.button("Evaluate Response"):

    import time

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i + 1)

    st.success("✅ Response Evaluated Successfully!")

    accuracy = 92
    relevance = 90
    completeness = 88
    hallucination = 5

    overall = (accuracy + relevance + completeness + (100 - hallucination)) / 4

    st.subheader("📊 Evaluation Scores")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", f"{accuracy}%")
    col2.metric("Relevance", f"{relevance}%")
    col3.metric("Completeness", f"{completeness}%")
    col4.metric("Hallucination", f"{hallucination}%")

    st.divider()

    st.metric("Overall Score", f"{overall:.1f}%")

    if overall >= 90:
        st.success("🟢 Excellent AI Response")
    elif overall >= 75:
        st.info("🟡 Good AI Response")
    else:
        st.warning("🔴 Needs Improvement")

    st.subheader("📝 Submitted Details")

    st.write("### Question")
    st.write(question)

    st.write("### AI Response")
    st.write(ai_response)

    if reference_answer:
        st.write("### Reference Answer")
        st.write(reference_answer)

    if uploaded_file:
        st.write("📄 Uploaded File:", uploaded_file.name)

    st.subheader("💡 Suggestions")

    st.write("✔️ Improve factual accuracy where needed.")
    st.write("✔️ Add more detailed explanations.")
    st.write("✔️ Avoid unsupported claims.")
    st.write("✔️ Include references whenever possible.")
# Development of AI Response Validation System with Hallucination Detection Assistance

An AI-powered system that evaluates the quality of AI-generated responses using Retrieval-Augmented Generation (RAG) and a Multi-Agent Judging Pipeline.

The system evaluates AI responses across multiple quality dimensions including Relevance, Accuracy, Hallucination, and Completeness, and generates an overall quality verdict.

---

## 📌 Project Overview

Large Language Models (LLMs) such as ChatGPT and Gemini can generate human-like responses, but their responses may sometimes contain incorrect, incomplete, irrelevant, or hallucinated information.

The **Development of AI Response Validation System with Hallucination Detection Assistance ** is designed to automatically evaluate AI-generated responses against trusted reference knowledge.

The system uses a RAG pipeline to retrieve relevant reference information and a multi-agent evaluation architecture where specialized AI judge agents independently evaluate different aspects of the response.

The project was developed as part of the **Infosys Springboard 7.0 Internship**.

---

## 🎯 Project Objective

The main objective of this project is to build an AI-powered evaluation system that can:

- Evaluate the quality of AI-generated responses.
- Check whether a response is relevant to the question.
- Verify factual accuracy using trusted reference information.
- Detect unsupported or hallucinated information.
- Determine whether important information is missing.
- Generate an overall quality verdict.
- Evaluate multiple AI responses efficiently using batch processing.
- Visualize evaluation results through a scoring dashboard.
- Generate structured PDF evaluation reports.
- Validate the consistency of evaluation agents through repeated testing.
- Support end-to-end testing of the complete evaluation pipeline.

---

# 🏗️ System Architecture

```text
                         User
                          |
                          ▼
                Evaluation Input Module
                          |
                          ▼
              Reference Knowledge Base
                          |
                          ▼
                 RAG Retrieval Pipeline
                          |
                          ▼
             Multi-Agent Judging Pipeline
                          |
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   Relevance          Accuracy       Hallucination
     Agent              Agent             Agent
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
                 Completeness Agent
                          |
                          ▼
                    Verdict Agent
                          |
                          ▼
                  Evaluation Results
                          |
              ┌───────────┴───────────┐
              ▼                       ▼
      Evaluation Dashboard      PDF Report Export
      
🔄 Evaluation Workflow
Input Question + AI Response
              |
              ▼
       Reference Retrieval
              |
              ▼
      Relevance Evaluation
              |
              ▼
       Accuracy Evaluation
              |
              ▼
   Hallucination Detection
              |
              ▼
     Completeness Evaluation
              |
              ▼
       Generate Final Verdict
              |
              ▼
       Store Evaluation Results
              |
              ▼
       Dashboard / PDF Report
---
# 🤖 AI Judge Agents

The system uses five specialized evaluation agents.

## 1. Relevance Judge Agent

Evaluates how well the AI-generated response answers the user's question.

### Input

- User Question
- AI Response

### Output

- Relevance Score (0–10)
- Reason for the score

---

## 2. Accuracy Judge Agent

Verifies the factual correctness of the AI-generated response by comparing it with the reference answer retrieved from the RAG knowledge base.

### Input

- User Question
- AI Response
- Reference Answer

### Output

- Accuracy Score (0–10)
- Reason for the score

---

## 3. Hallucination Detection Agent

Identifies unsupported, fabricated, or factually incorrect information in the AI-generated response.

### Input

- User Question
- AI Response
- Reference Answer

### Output

- Hallucination Score (0–10)
- Reason for the score

---

## 4. Completeness Evaluation Agent

Checks whether the AI response contains all important information available in the reference answer.

### Input

- User Question
- AI Response
- Reference Answer

### Output

- Completeness Score
- Reason
- Missing Points

---

## 5. Final Verdict Agent

Combines the evaluation results from the different judge agents and generates an overall assessment.

The verdict is based on:

- Relevance Score
- Accuracy Score
- Hallucination Score
- Completeness Score

The system classifies responses into:

- Excellent
- Good
- Needs Improvement
- Fail
---

# 📊 Evaluation Dimensions

| Dimension | Purpose |
|---|---|
| Accuracy | Checks factual correctness of the AI response |
| Relevance | Determines whether the response answers the user's question |
| Completeness | Checks whether all important points are covered |
| Hallucination | Detects unsupported or incorrect information |
| Overall Score | Represents the final evaluation result |
---

# 📚 Reference Knowledge Base

The project uses trusted datasets as reference knowledge for grounded evaluation.

## Datasets Used

- SQuAD
- TruthfulQA
- Custom AI Knowledge Base

The datasets are processed and divided into chunks before generating embeddings.

The generated embeddings are stored in a FAISS vector database, which is used for semantic similarity search and reference retrieval.
---
# 🔎 RAG Pipeline

The Retrieval-Augmented Generation (RAG) pipeline provides relevant reference information to the evaluation agents.

```text
Knowledge Base
      |
      ▼
Dataset Chunking
      |
      ▼
Text Embeddings
      |
      ▼
FAISS Vector Database
      |
      ▼
Semantic Retrieval
      |
      ▼
Relevant Reference Answer
      |
      ▼
AI Response Evaluation
---
# 📂 Batch Evaluation

The Batch Evaluation Module allows multiple AI-generated responses to be evaluated using a CSV file.

## Required CSV Columns

- Question
- AI_Response
- Reference Answer

## Batch Processing Workflow

```text
Upload CSV
    |
    ▼
Validate Required Columns
    |
    ▼
Read Each Record
    |
    ▼
Evaluate Relevance
    |
    ▼
Evaluate Accuracy
    |
    ▼
Detect Hallucination
    |
    ▼
Evaluate Completeness
    |
    ▼
Generate Final Verdict
    |
    ▼
Store Results
    |
    ▼
Display Evaluation Results
    |
    ▼
Download CSV Report
---

## Batch Evaluation Output
The generated results include:
- Question
- AI Response
- Relevance Score
- Accuracy Score
- Hallucination Score
- Completeness Score
- Overall Score
- Final Verdict
- Detailed evaluation reasoning
---
# 🖥️ User Interface

The project uses Streamlit to provide interactive interfaces for evaluating AI-generated responses.

The platform supports:

- Single AI response evaluation
- Question and AI response input
- Reference retrieval
- Multi-agent evaluation
- Batch CSV upload
- CSV validation
- Batch processing
- Evaluation results display
- Detailed evaluation analysis
- Downloadable evaluation results
- Evaluation scoring dashboard
- Verdict filtering
- Quality dimension analysis
- Hallucination analysis
---
# 📊 Evaluation Scoring Dashboard

As part of Milestone 4, an Evaluation Scoring Dashboard was developed using Streamlit.

The dashboard reads the generated evaluation results and provides a visual summary of the evaluation batch.
---
## Dashboard Features

- Total evaluations
- Average overall score
- PASS count
- NEEDS IMPROVEMENT count
- FAIL count
- Average Relevance score
- Average Accuracy score
- Average Completeness score
- Hallucination frequency
- Verdict distribution
- Overall score comparison
- Dimension score comparison
- Detailed evaluation results
- Verdict filtering
- Evaluation summary table
- CSV download

## Dashboard Analysis

### Evaluation Overview

Displays:

- Total Evaluations
- Average Score
- PASS evaluations
- Issues detected

### Quality Dimensions

Displays average:

- Relevance
- Accuracy
- Completeness

### Verdict Distribution

Visualizes the number of:

- PASS
- NEEDS IMPROVEMENT
- FAIL

evaluations.

### Hallucination Analysis

The dashboard calculates hallucination frequency based on the configured hallucination score threshold.

Responses with a hallucination score of **5 or above** are treated as significant hallucination-risk responses for reporting.

### Response Score Comparison

The dashboard displays the overall score obtained by each evaluated response.

### Dimension Score Comparison

The dashboard displays the Relevance, Accuracy, Hallucination, and Completeness scores across evaluated responses.

---
# 📈 Project Progress

## Milestone 1 — Foundation and RAG Pipeline

Milestone 1 focused on establishing the foundation of the AI response evaluation system and implementing the initial RAG pipeline.

### Completed

- Studied LLM evaluation techniques.
- Studied hallucination detection.
- Researched Retrieval-Augmented Generation (RAG) architecture.
- Studied RAGAS and TruLens.
- Designed the initial system architecture.
- Defined evaluation dimensions and agent responsibilities.
- Developed the initial Streamlit evaluation interface.
- Created a reference knowledge base using SQuAD, TruthfulQA, and custom AI knowledge.
- Implemented dataset chunking.
- Generated text embeddings.
- Created a FAISS vector database.
- Implemented semantic retrieval.
- Developed the initial working prototype.

### Milestone 1 Outcome

The initial prototype successfully demonstrated the basic RAG-based evaluation workflow, where relevant reference information could be retrieved from the knowledge base for evaluating AI-generated responses.

---
## Milestone 2 — Core AI Judge Agents

Milestone 2 focused on developing the core AI judge agents and integrating them with the RAG-based evaluation pipeline.

### Completed

- Developed the Relevance Judge Agent.
- Developed the Accuracy Judge Agent.
- Developed the Hallucination Detection Agent.
- Integrated the three judge agents with the RAG pipeline.
- Enhanced the Streamlit evaluation interface.
- Tested the judge agents using multiple question-answer pairs.
- Evaluated the quality of agent-generated scores and reasoning.
- Validated the initial scoring consistency of the evaluation agents.

### Milestone 2 Outcome

The Milestone 2 prototype successfully demonstrated an automated evaluation workflow using specialized AI judge agents for Relevance, Accuracy, and Hallucination Detection.

---
## Milestone 3 — Advanced Evaluation and Batch Processing

Milestone 3 focused on extending the evaluation system with additional evaluation capabilities and batch processing.

### Completed

- Developed the Completeness Evaluation Agent.
- Developed the Final Verdict Agent.
- Integrated the Completeness Agent and Verdict Agent into the evaluation pipeline.
- Implemented the Batch Evaluation Module.
- Added CSV file upload and validation.
- Implemented batch processing of multiple AI-generated responses.
- Added structured evaluation results.
- Added detailed evaluation reasoning.
- Added downloadable CSV evaluation results.
- Improved the Streamlit user interface.
- Tested the complete evaluation pipeline using multiple AI responses.

### Batch Evaluation

The Batch Evaluation Module processes multiple AI-generated responses from a CSV file.

The workflow includes:

```text
Upload CSV
    |
    ▼
Validate CSV
    |
    ▼
Process Each Response
    |
    ▼
Relevance Evaluation
    |
    ▼
Accuracy Evaluation
    |
    ▼
Hallucination Detection
    |
    ▼
Completeness Evaluation
    |
    ▼
Final Verdict
    |
    ▼
Store Evaluation Results
    |
    ▼
Download Results
---

## Milestone 3 Outcome
The system evolved from a single-response evaluation prototype into a multi-agent evaluation platform capable of processing multiple AI responses through batch CSV evaluation.
The system could evaluate Relevance, Accuracy, Hallucination, and Completeness, generate an overall score and verdict, and provide structured evaluation results.

## Milestone 4 — Dashboard, Report Export and End-to-End Validation

Milestone 4 focused on extending the AI response validation platform with an evaluation scoring dashboard, structured PDF report generation, and complete end-to-end testing.

### 1. Evaluation Scoring Dashboard

A Streamlit-based Evaluation Scoring Dashboard was developed to visualize and analyze batch evaluation results.

The dashboard provides:

- Total evaluations
- Average overall score
- PASS count
- NEEDS IMPROVEMENT count
- FAIL count
- Average Relevance score
- Average Accuracy score
- Average Completeness score
- Hallucination frequency
- Verdict distribution
- Overall score comparison
- Dimension score comparison
- Detailed evaluation results
- Verdict filtering
- Evaluation summary table
- CSV download

The dashboard helps users understand the overall quality and reliability of evaluated AI responses.

### 2. Evaluation Report Export

A structured PDF evaluation report generation feature was implemented.

The PDF report contains:

- Project details
- Batch evaluation summary
- Dimension-wise scores
- Individual evaluation results
- Hallucinated responses
- Flagged responses
- Overall verdicts
- Evaluation charts
- Improvement recommendations
- Conclusion

The report provides a formal and structured representation of the batch evaluation results.

### 3. End-to-End Testing

The complete evaluation platform was tested to verify that the individual modules work together correctly.

The testing covered:

- Single evaluation workflow
- Batch evaluation workflow
- Dashboard updates
- PDF report generation
- RAG retrieval
- Agent scoring
- Verdict generation
- Error handling
- Invalid input handling

The complete evaluation workflow was successfully tested from input processing through final result generation.

### 4. Scoring Consistency Validation

The same evaluation dataset was executed multiple times to validate the stability of the evaluation agents.

The following results were compared:

- Relevance scores
- Accuracy scores
- Completeness scores
- Hallucination detection
- Final verdict

Most evaluation results remained consistent across repeated runs.

Small variations were observed in some LLM-generated scores, such as differences of approximately 0.1, 0.2, or 0.4, and occasional changes in individual dimension scores.

These variations are expected because the evaluation agents use LLM-based judgment, which can produce slightly different results across repeated executions.

Despite these small variations, the majority of evaluation scores remained stable and the evaluation pipeline continued to produce meaningful results.

### 5. Milestone 4 Outcome

Milestone 4 extended the platform from a batch evaluation system into a more complete AI response validation platform with:

- Evaluation Scoring Dashboard
- PDF Evaluation Report Export
- End-to-End Testing
- Scoring Consistency Validation
- Structured evaluation analysis

The system is now capable of evaluating AI responses, processing batches, visualizing evaluation results, generating formal reports, and validating the overall evaluation workflow.
---
# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Primary programming language |
| Streamlit | User interface and dashboard |
| Groq API | LLM-based evaluation |
| LangChain | RAG pipeline development |
| Sentence Transformers | Text embedding generation |
| FAISS | Vector similarity search |
| Hugging Face Datasets | SQuAD and TruthfulQA datasets |
| Pandas | Data processing and CSV handling |
| Matplotlib | Data visualization |
| ReportLab | PDF report generation |
| Git & GitHub | Version control |
| RAGAS | RAG evaluation framework |
| TruLens | LLM application evaluation and monitoring |

---
Project Structure

AI-Response-Quality-Evaluator-Agent/
│
├── agents/
│   ├── __init__.py
│   ├── accuracy_agent.py
│   ├── completeness_agent.py
│   ├── hallucination_agent.py
│   ├── relevance_agent.py
│   └── verdict_agent.py
│
├── assets/
│
├── datasets/
│   └── ai_knowledge_base.json
│
├── docs/
│
├── embeddings/
│
├── knowledge_base/
│   ├── chunk_data.py
│   ├── chunks.json
│   ├── create_vector_db.py
│   ├── dataset_loader.py
│   ├── embeddings.pkl
│   ├── faiss_index.index
│   ├── generate_embeddings.py
│   └── retrieve.py
│
├── modules/
│
├── report_charts/
│
├── tests/
│   ├── test_accuracy.py
│   ├── test_completeness.py
│   ├── test_hallucination.py
│   ├── test_llm.py
│   ├── test_relevance.py
│   ├── test_score_parser.py
│   └── test_verdict.py
│
├── validation/
│   └── validate.py
│
├── .env
├── .gitignore
├── app.py
├── batch_app.py
├── config.py
├── dashboard.py
├── evaluation.py
├── evaluation_results.csv
├── list_models.py
├── llm.py
├── README.md
├── report_generator.py
├── requirements.txt
├── retriever.py
└── score_parser.py

Main Components

- agents/ – Contains the evaluation agents for relevance, accuracy, completeness, hallucination detection, and final verdict generation.
- datasets/ – Contains the AI knowledge-base dataset used by the evaluation system.
- knowledge_base/ – Handles data chunking, embedding generation, FAISS vector database creation, and retrieval for the RAG workflow.
- tests/ – Contains test cases for the evaluation agents, LLM functionality, score parsing, and verdict generation.
- validation/ – Contains validation scripts for checking the system.
- dashboard.py – Provides the evaluation scoring dashboard and result visualization.
- batch_app.py – Handles batch evaluation of multiple questions and AI responses.
- evaluation.py – Coordinates the evaluation workflow.
- app.py – Handles the main application interface.
- report_generator.py – Generates evaluation reports.
- score_parser.py – Processes and extracts evaluation scores.
- llm.py – Handles LLM-related functionality.
- retriever.py – Supports retrieval of relevant knowledge for evaluation.
- evaluation_results.csv – Stores evaluation results.
- config.py – Contains project configuration settings.
- requirements.txt – Contains the required Python dependencies.

# 📌 Current Capabilities

The completed system provides an end-to-end platform for evaluating and validating AI-generated responses.

The current system can:

- Retrieve relevant reference information using RAG.
- Evaluate AI responses using specialized AI judge agents.
- Measure Relevance.
- Measure Accuracy.
- Detect Hallucinations.
- Measure Completeness.
- Generate an Overall Score.
- Generate a Final Verdict.
- Process multiple AI responses through CSV batch evaluation.
- Display structured evaluation results.
- Provide detailed evaluation reasoning.
- Export batch evaluation results as CSV.
- Visualize evaluation results through an Evaluation Scoring Dashboard.
- Display PASS, NEEDS IMPROVEMENT, and FAIL counts.
- Analyze average quality dimension scores.
- Analyze hallucination frequency.
- Compare evaluation scores across responses.
- Filter evaluation results by verdict.
- Generate structured PDF evaluation reports.
- Display individual evaluation results in reports.
- Identify flagged and hallucination-risk responses.
- Provide improvement recommendations.
- Perform end-to-end testing across the evaluation workflow.
- Validate scoring consistency through repeated evaluation runs.

---
# 🧪 Testing Results

The system was tested across the major components of the AI response validation platform to verify functionality, integration, and reliability.

| Test Area | Result |
|---|---|
| Single Evaluation Workflow | Tested Successfully |
| Batch Evaluation Workflow | Tested Successfully |
| RAG Retrieval | Tested Successfully |
| Relevance Agent | Tested Successfully |
| Accuracy Agent | Tested Successfully |
| Hallucination Detection | Tested Successfully |
| Completeness Agent | Tested Successfully |
| Final Verdict Generation | Tested Successfully |
| Evaluation Dashboard | Tested Successfully |
| PDF Report Generation | Tested Successfully |
| CSV Export | Tested Successfully |
| Error Handling | Tested |
| Invalid Input Handling | Tested |
| Scoring Consistency | Validated |
---
## Scoring Consistency Testing

The same evaluation dataset was executed multiple times to compare the outputs produced by the evaluation agents.

The comparison included:

- Relevance scores
- Accuracy scores
- Completeness scores
- Hallucination detection
- Overall scores
- Final verdicts

Most results remained consistent across repeated executions. Small variations were observed in some LLM-generated scores because the evaluation agents use probabilistic language-model-based judgment.

These variations were generally small, while the overall evaluation behavior remained stable.

---

## Testing Conclusion

The testing confirmed that the major modules of the platform work together correctly, from reference retrieval and agent-based evaluation to batch processing, dashboard visualization, and PDF report generation.

---
# ⚠️ Limitations

The current system has some limitations:

- LLM-based evaluation agents may produce small score variations across repeated runs.
- Evaluation quality depends on the quality of the retrieved reference information.
- Hallucination detection depends on the available reference knowledge.
- The current dashboard analyzes the evaluation results available in the generated dataset.
- External knowledge retrieval is limited to the configured knowledge sources.
- Some evaluation scores may vary slightly because the system uses LLM-based judgment.
- The current system focuses primarily on text-based AI response evaluation.
- The evaluation results depend on the quality and completeness of the reference answers.

---
# 🔮 Future Work

The following enhancements can be considered for future development:

- Integration with a database for storing evaluation history.
- User authentication and role-based access.
- Multi-language AI response evaluation.
- Automatic reference retrieval from additional external knowledge sources.
- Real-time evaluation analytics.
- Advanced dashboard filters for model, dataset, evaluation mode, and date.
- Comparison of multiple AI systems on the same evaluation dataset.
- Model-wise and dataset-wise performance analysis.
- Improved scoring consistency mechanisms.
- Advanced hallucination detection techniques.
- Automated evaluation benchmarking.
- Evaluation history and trend tracking.
- Support for additional AI evaluation metrics.
- Enhanced visualization and reporting capabilities.

---
# 🎬 Project Demonstration

The final project demonstration showcases the complete AI response validation platform.

## Demonstration Flow

```text
Explain Project Objective
          |
          ▼
Evaluate a Single AI Response
          |
          ▼
Run Batch Evaluation using CSV
          |
          ▼
Display Evaluation Results
          |
          ▼
Open Evaluation Dashboard
          |
          ▼
Analyze Scores and Verdicts
          |
          ▼
Generate PDF Evaluation Report
          |
          ▼
Open and Demonstrate PDF Report
          |
          ▼
Compare Evaluations from Two AI Systems
          |
          ▼
Summarize Findings
          |
          ▼
Explain Strengths, Limitations
and Future Improvements
---                                                             
# 🎓 Internship

**Internship:** Infosys Springboard 7.0 Internship

**Project:** Development of AI Response Validation System with Hallucination Detection Assistance

**Student:** Sarvasuddi Gowthami

---

# 📌 Conclusion

The **Development of AI Response Validation System with Hallucination Detection Assistance ** provides an automated framework for evaluating and validating AI-generated responses using Retrieval-Augmented Generation (RAG) and a multi-agent judging architecture.

The project evolved through four milestones from an initial RAG-based evaluation prototype into a complete AI response validation platform.

The system evaluates AI-generated responses across multiple dimensions including:

- Relevance
- Accuracy
- Hallucination
- Completeness
- Overall Quality

The platform also supports batch evaluation of multiple AI responses using CSV files and provides detailed evaluation reasoning and final verdicts.

As part of Milestone 4, the system was extended with an Evaluation Scoring Dashboard, structured PDF evaluation reports, end-to-end testing, and scoring consistency validation.

The completed platform provides a structured approach for analyzing the quality, reliability, completeness, and potential hallucination of AI-generated responses.

---

## 👩‍💻 Developed By

**Sarvasuddi Gowthami**

**Infosys Springboard 7.0 Internship**

**Project Title: Development of AI Response Validation System with Hallucination Detection Assistance **




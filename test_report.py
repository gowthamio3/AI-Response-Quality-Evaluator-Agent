import pandas as pd
from report_generator import generate_pdf_report


# Change this only if your CSV has a different filename
CSV_FILE = "evaluation_results.csv"


# Read evaluation results
df = pd.read_csv(CSV_FILE)


# Generate PDF
generate_pdf_report(
    df,
    "test_evaluation_report.pdf"
)
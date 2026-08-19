import os
import re
import pandas as pd
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)


PROJECT_TITLE = (
    "Development of AI Response Validation System "
    "with Hallucination Detection Assistance"
)

GROUP_NAME = "Group 1"
CHART_DIR = "report_charts"

os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def find_column(df, names):
    normalized = {
        str(c).strip().lower().replace("_", " "): c
        for c in df.columns
    }

    for name in names:
        key = name.strip().lower().replace("_", " ")
        if key in normalized:
            return normalized[key]

    return None


def number(value):
    if pd.isna(value):
        return None

    match = re.search(r"-?\d+(?:\.\d+)?", str(value))

    if match:
        return float(match.group())

    return None


def text(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def verdict(value):
    if pd.isna(value):
        return ""

    value = str(value).strip().upper()
    value = value.replace("_", " ")

    if value.startswith("PASS"):
        return "PASS"

    if "IMPROVEMENT" in value:
        return "NEEDS IMPROVEMENT"

    if value.startswith("FAIL"):
        return "FAIL"

    return value


def page_number(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica", 8)

    canvas.drawString(
        16 * mm,
        9 * mm,
        PROJECT_TITLE
    )

    canvas.drawRightString(
        194 * mm,
        9 * mm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# CHARTS
# ============================================================

def create_verdict_chart(pass_count, improvement_count, fail_count):

    path = os.path.join(
        CHART_DIR,
        "verdict_distribution.png"
    )

    labels = [
        "PASS",
        "NEEDS IMPROVEMENT",
        "FAIL"
    ]

    values = [
        pass_count,
        improvement_count,
        fail_count
    ]

    plt.figure(figsize=(7.5, 4))

    bars = plt.bar(labels, values)

    plt.title(
        "Evaluation Verdict Distribution",
        fontweight="bold"
    )

    plt.ylabel("Number of Evaluations")

    maximum = max(values) if values else 1

    plt.ylim(0, maximum + 2)

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.1,
            str(value),
            ha="center",
            fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


def create_dimension_chart(values):

    path = os.path.join(
        CHART_DIR,
        "dimension_scores.png"
    )

    labels = list(values.keys())
    scores = list(values.values())

    plt.figure(figsize=(7.5, 4))

    bars = plt.bar(labels, scores)

    plt.title(
        "Average Dimension Scores",
        fontweight="bold"
    )

    plt.ylabel("Score / 10")
    plt.ylim(0, 10)

    for bar, value in zip(bars, scores):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.15,
            f"{value:.2f}",
            ha="center",
            fontweight="bold"
        )

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


def create_overall_chart(overall_scores):

    path = os.path.join(
        CHART_DIR,
        "overall_scores.png"
    )

    x = list(range(1, len(overall_scores) + 1))

    plt.figure(figsize=(8, 4))

    bars = plt.bar(x, overall_scores)

    plt.title(
        "Overall Score by Evaluation",
        fontweight="bold"
    )

    plt.xlabel("Evaluation Number")
    plt.ylabel("Score / 10")
    plt.ylim(0, 10)

    for bar, value in zip(bars, overall_scores):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.1,
            f"{value:.1f}",
            ha="center",
            fontsize=7
        )

    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

    return path


# ============================================================
# MAIN REPORT FUNCTION
# ============================================================

def generate_pdf_report(
    df,
    output_path="test_evaluation_report.pdf"
):

    if df is None or df.empty:
        raise ValueError("Evaluation CSV contains no data.")

    df = df.copy()
    # --------------------------------------------------------
    # FIND CSV COLUMNS
    # --------------------------------------------------------

    question_col = find_column(
        df,
        ["Question", "Prompt", "Query"]
    )

    response_col = find_column(
        df,
        [
            "AI Response",
            "AI_Response",
            "Response",
            "Answer"
        ]
    )

    reference_col = find_column(
        df,
        [
            "Reference Answer",
            "Reference_Answer",
            "Reference"
        ]
    )

    relevance_col = find_column(
        df,
        ["Relevance", "Relevance Score"]
    )

    accuracy_col = find_column(
        df,
        ["Accuracy", "Accuracy Score"]
    )

    hallucination_col = find_column(
        df,
        ["Hallucination", "Hallucination Score"]
    )

    completeness_col = find_column(
        df,
        ["Completeness", "Completeness Score"]
    )

    overall_col = find_column(
        df,
        [
            "Overall Score",
            "Overall",
            "Final Score"
        ]
    )

    verdict_col = find_column(
        df,
        [
            "Verdict",
            "Final Verdict",
            "Result"
        ]
    )

    # --------------------------------------------------------
    # PREPARE EVALUATIONS
    # --------------------------------------------------------

    evaluations = []

    for i, row in df.iterrows():

        relevance = (
            number(row[relevance_col])
            if relevance_col else None
        )

        accuracy = (
            number(row[accuracy_col])
            if accuracy_col else None
        )

        hallucination = (
            number(row[hallucination_col])
            if hallucination_col else None
        )

        completeness = (
            number(row[completeness_col])
            if completeness_col else None
        )

        overall = (
            number(row[overall_col])
            if overall_col else None
        )

        if overall is None:

            scores = [
                x for x in [
                    relevance,
                    accuracy,
                    completeness
                ]
                if x is not None
            ]

            if scores:
                overall = sum(scores) / len(scores)

        final_verdict = (
            verdict(row[verdict_col])
            if verdict_col else ""
        )

        # Only fallback if Verdict is unavailable
        if not final_verdict:

            if overall is not None:

                if overall >= 8:
                    final_verdict = "PASS"

                elif overall >= 5:
                    final_verdict = "NEEDS IMPROVEMENT"

                else:
                    final_verdict = "FAIL"

            else:
                final_verdict = "NEEDS IMPROVEMENT"

        evaluations.append({
            "number": len(evaluations) + 1,
            "question": (
                text(row[question_col])
                if question_col else ""
            ),
            "response": (
                text(row[response_col])
                if response_col else ""
            ),
            "reference": (
                text(row[reference_col])
                if reference_col else ""
            ),
            "relevance": relevance,
            "accuracy": accuracy,
            "hallucination": hallucination,
            "completeness": completeness,
            "overall": overall,
            "verdict": final_verdict
        })

    total = len(evaluations)

    # --------------------------------------------------------
    # SUMMARY COUNTS
    # --------------------------------------------------------

    pass_count = sum(
        x["verdict"] == "PASS"
        for x in evaluations
    )

    improvement_count = sum(
        x["verdict"] == "NEEDS IMPROVEMENT"
        for x in evaluations
    )

    fail_count = sum(
        x["verdict"] == "FAIL"
        for x in evaluations
    )

    def average(key):

        values = [
            x[key]
            for x in evaluations
            if x[key] is not None
        ]

        if not values:
            return 0

        return sum(values) / len(values)

    relevance_avg = average("relevance")
    accuracy_avg = average("accuracy")
    hallucination_avg = average("hallucination")
    completeness_avg = average("completeness")
    overall_avg = average("overall")

    # --------------------------------------------------------
    # HALLUCINATED RESPONSES
    #
    # Existing project scoring uses hallucination score.
    # We flag scores >= 5 for detailed reporting.
    # --------------------------------------------------------

    hallucinated = [
        x for x in evaluations
        if (
            x["hallucination"] is not None
            and x["hallucination"] >= 5
        )
    ]

    hallucination_frequency = (
        len(hallucinated) / total * 100
        if total
        else 0
    )

    # --------------------------------------------------------
    # FLAGGED RESPONSES
    # --------------------------------------------------------

    flagged = [
        x for x in evaluations
        if (
            x["verdict"] in [
                "FAIL",
                "NEEDS IMPROVEMENT"
            ]
            or (
                x["hallucination"] is not None
                and x["hallucination"] >= 5
            )
        )
    ]

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    verdict_chart = create_verdict_chart(
        pass_count,
        improvement_count,
        fail_count
    )

    dimension_chart = create_dimension_chart({
        "Relevance": relevance_avg,
        "Accuracy": accuracy_avg,
        "Completeness": completeness_avg,
        "Hallucination": hallucination_avg,
        "Overall": overall_avg
    })

    overall_chart = create_overall_chart([
        x["overall"] if x["overall"] is not None else 0
        for x in evaluations
    ])

    # ========================================================
    # PDF SETUP
    # ========================================================

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        fontSize=19,
        leading=23,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17365D"),
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#555555"),
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "Heading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=15,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=5,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=11,
        spaceAfter=3
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=7.5,
        leading=9.5,
        spaceAfter=2
    )

    story = []

    # ========================================================
    # 1. PROJECT DETAILS
    # ========================================================

    story.append(
        Paragraph(
            PROJECT_TITLE,
            title_style
        )
    )

    story.append(
        Paragraph(
            "Evaluation Report Export — Milestone 4",
            subtitle_style
        )
    )

    project_data = [
        ["Project Title", PROJECT_TITLE],
        ["Group", GROUP_NAME],
        ["Milestone", "Milestone 4"],
        ["Report Type", "Batch Evaluation Report"],
        ["Format", "PDF"],
        ["Total Evaluations", str(total)]
    ]

    project_table = Table(
        project_data,
        colWidths=[45 * mm, 130 * mm]
    )

    project_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1),
             colors.HexColor("#EAF0F8")),
            ("FONTNAME", (0, 0), (0, -1),
             "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1),
             0.35, colors.HexColor("#B8C4D4")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
        ])
    )

    story.append(project_table)
    story.append(Spacer(1, 5 * mm))

    # ========================================================
    # 2. BATCH SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "1. Batch Evaluation Summary",
            heading_style
        )
    )

    summary_data = [
        ["Metric", "Result"],
        ["Total Evaluations", str(total)],
        ["PASS", str(pass_count)],
        ["NEEDS IMPROVEMENT", str(improvement_count)],
        ["FAIL", str(fail_count)],
        ["Average Overall Score", f"{overall_avg:.2f}/10"],
        ["Hallucination Frequency",
         f"{hallucination_frequency:.1f}%"]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[80 * mm, 50 * mm]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1),
             0.35, colors.HexColor("#C5CDD8")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
        ])
    )

    story.append(summary_table)
    story.append(Spacer(1, 4 * mm))

    # ========================================================
    # 3. DIMENSION-WISE SCORES
    # ========================================================

    story.append(
        Paragraph(
            "2. Dimension-wise Score Analysis",
            heading_style
        )
    )

    dimension_data = [
        ["Dimension", "Average Score"],
        ["Relevance", f"{relevance_avg:.2f}/10"],
        ["Accuracy", f"{accuracy_avg:.2f}/10"],
        ["Completeness", f"{completeness_avg:.2f}/10"],
        ["Hallucination", f"{hallucination_avg:.2f}/10"],
        ["Overall Score", f"{overall_avg:.2f}/10"]
    ]

    dimension_table = Table(
        dimension_data,
        colWidths=[80 * mm, 50 * mm]
    )

    dimension_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1),
             0.35, colors.HexColor("#C5CDD8")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
        ])
    )

    story.append(dimension_table)
    story.append(Spacer(1, 4 * mm))
    story.append(PageBreak())
    # ========================================================
    # 4. EVALUATION CHARTS
    # ========================================================

    story.append(
        Paragraph(
            "3. Evaluation Charts",
            heading_style
        )
    )

    # Verdict distribution chart
    story.append(
        Image(
            verdict_chart,
            width=145 * mm,
            height=68 * mm
        )
    )

    story.append(
        Paragraph(
            "The chart shows the distribution of PASS, NEEDS IMPROVEMENT, "
            "and FAIL verdicts in the evaluation batch.",
            small_style
        )
    )

    story.append(Spacer(1, 3 * mm))

    # Dimension score chart
    story.append(
        Image(
            dimension_chart,
            width=145 * mm,
            height=68 * mm
        )
    )

    story.append(
        Paragraph(
            "The chart compares the average scores across the evaluation "
            "dimensions.",
            small_style
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 5. OVERALL SCORE CHART
    # ========================================================

    story.append(
        Paragraph(
            "4. Overall Score Trend",
            heading_style
        )
    )

    story.append(
        Image(
            overall_chart,
            width=155 * mm,
            height=72 * mm
        )
    )

    story.append(Spacer(1, 4 * mm))

    story.append(
        Paragraph(
            "The chart shows the overall score obtained for each "
            "evaluation in the batch.",
            normal_style
        )
    )

    story.append(PageBreak())

    # ========================================================
    # 6. INDIVIDUAL EVALUATION RESULTS
    # ========================================================

    story.append(
        Paragraph(
            "5. Individual Evaluation Results",
            heading_style
        )
    )

    for item in evaluations:

        story.append(
            Paragraph(
                f"<b>Evaluation {item['number']}</b>",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Question:</b> {item['question']}",
                small_style
            )
        )

        story.append(
            Paragraph(
                f"<b>AI Response:</b> {item['response']}",
                small_style
            )
        )

        if item["reference"]:
            story.append(
                Paragraph(
                    f"<b>Reference Answer:</b> {item['reference']}",
                    small_style
                )
            )

        score_data = [
            [
                "Relevance",
                "Accuracy",
                "Completeness",
                "Hallucination",
                "Overall"
            ],
            [
                f"{item['relevance']:.1f}/10"
                if item["relevance"] is not None else "N/A",

                f"{item['accuracy']:.1f}/10"
                if item["accuracy"] is not None else "N/A",

                f"{item['completeness']:.1f}/10"
                if item["completeness"] is not None else "N/A",

                f"{item['hallucination']:.1f}/10"
                if item["hallucination"] is not None else "N/A",

                f"{item['overall']:.1f}/10"
                if item["overall"] is not None else "N/A"
            ]
        ]

        score_table = Table(
            score_data,
            colWidths=[32 * mm] * 5
        )

        score_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#EAF0F8")),

                ("FONTNAME", (0, 0), (-1, 0),
                 "Helvetica-Bold"),

                ("FONTSIZE", (0, 0), (-1, -1), 7),

                ("ALIGN", (0, 0), (-1, -1),
                 "CENTER"),

                ("GRID", (0, 0), (-1, -1),
                 0.3, colors.HexColor("#C5CDD8")),

                ("TOPPADDING", (0, 0), (-1, -1), 3),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 3)
            ])
        )

        story.append(score_table)

        story.append(
            Paragraph(
                f"<b>Overall Verdict:</b> {item['verdict']}",
                small_style
            )
        )

        story.append(Spacer(1, 5 * mm))

    # ========================================================
    # 7. HALLUCINATED RESPONSES
    # ========================================================

    story.append(
        Paragraph(
            "6. Hallucinated Responses",
            heading_style
        )
    )

    if hallucinated:

        for item in hallucinated:
            story.append(
                Paragraph(
                    f"<b>Evaluation {item['number']}</b>",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Question:</b> {item['question']}",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Hallucination Score:</b> "
                    f"{item['hallucination']:.1f}/10",
                    small_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Verdict:</b> {item['verdict']}",
                    small_style
                )
            )

            story.append(Spacer(1, 3 * mm))

    else:

        story.append(
            Paragraph(
                "No responses crossed the configured hallucination "
                "flagging threshold in this batch.",
                normal_style
            )
        )

    story.append(Spacer(1, 4 * mm))

    # ========================================================
    # 8. FLAGGED RESPONSES
    # ========================================================

    story.append(
        Paragraph(
            "7. Flagged Responses",
            heading_style
        )
    )

    if flagged:

        flagged_data = [
            [
                "Evaluation",
                "Overall",
                "Verdict",
                "Hallucination",
                "Reason"
            ]
        ]

        for item in flagged:

            reasons = []

            if item["verdict"] == "FAIL":
                reasons.append("FAIL")

            elif item["verdict"] == "NEEDS IMPROVEMENT":
                reasons.append("Needs improvement")

            if (
                    item["hallucination"] is not None
                    and item["hallucination"] >= 5
            ):
                reasons.append("Hallucination flag")

            flagged_data.append([
                str(item["number"]),

                (
                    f"{item['overall']:.1f}/10"
                    if item["overall"] is not None
                    else "N/A"
                ),

                item["verdict"],

                (
                    f"{item['hallucination']:.1f}/10"
                    if item["hallucination"] is not None
                    else "N/A"
                ),

                ", ".join(reasons)
            ])

        flagged_table = Table(
            flagged_data,
            colWidths=[
                22 * mm,
                25 * mm,
                42 * mm,
                30 * mm,
                50 * mm
            ],
            repeatRows=1
        )

        flagged_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0),
                 colors.HexColor("#17365D")),
                ("TEXTCOLOR", (0, 0), (-1, 0),
                 colors.white),
                ("FONTNAME", (0, 0), (-1, 0),
                 "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("GRID", (0, 0), (-1, -1),
                 0.3, colors.HexColor("#C5CDD8")),
                ("VALIGN", (0, 0), (-1, -1),
                 "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
            ])
        )

        story.append(flagged_table)

    else:

        story.append(
            Paragraph(
                "No responses were flagged in this batch.",
                normal_style
            )
        )

    story.append(PageBreak())

    # ========================================================
    # 9. OVERALL VERDICTS
    # ========================================================

    story.append(
        Paragraph(
            "8. Overall Verdicts",
            heading_style
        )
    )

    verdict_data = [
        ["Verdict", "Count", "Percentage"],
        [
            "PASS",
            str(pass_count),
            f"{pass_count / total * 100:.1f}%"
            if total else "0%"
        ],
        [
            "NEEDS IMPROVEMENT",
            str(improvement_count),
            f"{improvement_count / total * 100:.1f}%"
            if total else "0%"
        ],
        [
            "FAIL",
            str(fail_count),
            f"{fail_count / total * 100:.1f}%"
            if total else "0%"
        ]
    ]

    verdict_table = Table(
        verdict_data,
        colWidths=[70 * mm, 35 * mm, 45 * mm]
    )

    verdict_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#17365D")),
            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),
            ("FONTNAME", (0, 0), (-1, 0),
             "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1),
             "CENTER"),
            ("GRID", (0, 0), (-1, -1),
             0.35, colors.HexColor("#C5CDD8")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )

    story.append(verdict_table)
    story.append(Spacer(1, 5 * mm))

    story.append(
        Paragraph(
            f"The batch contains {pass_count} PASS, "
            f"{improvement_count} NEEDS IMPROVEMENT, and "
            f"{fail_count} FAIL evaluations.",
            normal_style
        )
    )

    # ========================================================
    # 10. IMPROVEMENT RECOMMENDATIONS
    # ========================================================

    story.append(
        Paragraph(
            "9. Improvement Recommendations",
            heading_style
        )
    )

    recommendations = []

    if relevance_avg < 7:
        recommendations.append(
            "Improve relevance by ensuring responses directly address "
            "the user's question."
        )

    if accuracy_avg < 7:
        recommendations.append(
            "Improve factual accuracy by validating important claims "
            "against reliable retrieved information."
        )

    if completeness_avg < 7:
        recommendations.append(
            "Improve completeness by including the important points "
            "expected in the reference answer."
        )

    if hallucination_avg >= 5:
        recommendations.append(
            "Reduce hallucinated or unsupported information by "
            "strengthening retrieval grounding and verification."
        )

    if fail_count > 0:
        recommendations.append(
            f"Review the {fail_count} failed response(s) and identify "
            "the recurring causes of poor evaluation scores."
        )

    if improvement_count > 0:
        recommendations.append(
            f"Review the {improvement_count} responses marked "
            "NEEDS IMPROVEMENT and improve their weak dimensions."
        )

    if not recommendations:
        recommendations.append(
            "Continue monitoring response quality and maintain "
            "reference-grounded evaluation."
        )

    for i, recommendation in enumerate(
            recommendations,
            1
    ):
        story.append(
            Paragraph(
                f"<b>{i}.</b> {recommendation}",
                normal_style
            )
        )

    story.append(Spacer(1, 4 * mm))

    story.append(
        Paragraph(
            "<b>Conclusion:</b> "
            "This report provides a structured summary of the batch "
            "evaluation, including project details, evaluation results, "
            "dimension-wise scores, hallucination analysis, flagged "
            "responses, verdict distribution, charts, and improvement "
            "recommendations.",
            normal_style
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        story,
        onFirstPage=page_number,
        onLaterPages=page_number
    )

    print("\n======================================")
    print("FINAL PDF REPORT GENERATED")
    print("======================================")
    print(f"File: {os.path.abspath(output_path)}")
    print(f"Total Evaluations : {total}")
    print(f"PASS              : {pass_count}")
    print(f"NEEDS IMPROVEMENT : {improvement_count}")
    print(f"FAIL              : {fail_count}")
    print(f"Average Score     : {overall_avg:.2f}/10")
    print(f"Hallucinated      : {len(hallucinated)}")
    print(f"Flagged           : {len(flagged)}")
    print("======================================\n")

    return output_path
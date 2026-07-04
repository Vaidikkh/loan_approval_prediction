from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime


def generate_pdf(data, filename="Loan_Prediction_Report.pdf"):
    """
    data = {
        "model": "...",
        "income": "...",
        "credit_score": "...",
        "loan_amount": "...",
        "points": "...",
        "result": "..."
    }
    """

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # ---------------- Title ----------------

    title = Paragraph("<b><font size=20>Smart Loan Predictor</font></b>", styles["Title"])
    subtitle = Paragraph(
        "Machine Learning Loan Approval Prediction Report",
        styles["Heading2"]
    )

    elements.append(title)
    elements.append(subtitle)
    elements.append(Spacer(1, 20))

    # ---------------- Date ----------------

    date = Paragraph(
        f"<b>Generated On:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        styles["Normal"]
    )

    elements.append(date)
    elements.append(Spacer(1, 20))

    # ---------------- Table ----------------

    table_data = [

        ["Field", "Value"],

        ["Prediction Model", data["model"]],

        ["Annual Income", str(data["income"])],

        ["Credit Score", str(data["credit_score"])],

        ["Loan Amount", str(data["loan_amount"])],

        ["Credit Points", str(data["points"])],

        ["Prediction", data["result"]],

    ]

    table = Table(table_data, colWidths=[180, 280])

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E40AF")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EAF2FF")),

            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 0), (-1, -1), 11),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 8),

        ])

    )

    elements.append(table)

    elements.append(Spacer(1, 30))

    # ---------------- Recommendation ----------------

    if "Approved" in data["result"]:

        recommendation = (
            "<font color='green'><b>Recommendation:</b></font><br/>"
            "The applicant satisfies the model requirements and has a "
            "high probability of loan approval."
        )

    else:

        recommendation = (
            "<font color='red'><b>Recommendation:</b></font><br/>"
            "The applicant may not meet the approval criteria. "
            "Improving the credit score or financial profile may help."
        )

    elements.append(Paragraph(recommendation, styles["BodyText"]))

    elements.append(Spacer(1, 40))

    # ---------------- Footer ----------------

    footer = Paragraph(

        "<b>Developed By:</b> Vaidik Khandelwal<br/>"
        "B.Tech CSE (AI)<br/>"
        "Smart Loan Predictor",

        styles["Normal"]

    )

    elements.append(footer)

    # ---------------- Build PDF ----------------

    doc.build(elements)

    return filename
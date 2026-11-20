"""
Generates the daily A4 nutrition-plan sheet for Stefano's Kickstart phase.
Usage: edit the CONFIG block below for the day, then run.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

# ---------------- CONFIG (change per day) ----------------
OUT_PATH = "/home/user/Metabolic/scripts/tagesplan.pdf"
DATE_STR = "Freitag, 20. November 2026"
DAY_TYPE = "Krafttag"
TARGET_P, TARGET_F, TARGET_C, TARGET_KCAL = 190, 60, 90, 1660

MEALS = [
    {
        "name": "Frühstück",
        "items": [
            "4 ganze Eier + 2 Eiklar",
            "150g Spinat (gedünstet)",
            "40g Haferflocken",
        ],
        "p": 42, "f": 24, "c": 29,
    },
    {
        "name": "Mittag",
        "items": [
            "220g Putenbrust",
            "Großer Salat (Rucola/Tomate/Gurke/Paprika, ~300g)",
            "½ Avocado (50g)",
            "1 TL Olivenöl als Dressing",
        ],
        "p": 68, "f": 15, "c": 14,
    },
    {
        "name": "Abend (vor 21 Uhr)",
        "items": [
            "220g mageres Rinderfilet",
            "250g gedünstetes Gemüse (Brokkoli/Zucchini)",
            "80g Quinoa",
            "1 EL Olivenöl",
        ],
        "p": 78, "f": 23, "c": 30,
    },
]

RULES = [
    "3 Mahlzeiten/Tag, mind. 5h Pause dazwischen",
    "Mit 1-2 Bissen Eiweiß beginnen",
    "Pro Mahlzeit nur eine Eiweißart",
    "Nichts nach 21 Uhr",
    "3,4L Wasser über den Tag (erstes Glas direkt nach dem Aufstehen)",
    "Kein Alkohol",
]
# -----------------------------------------------------------

ink = colors.HexColor("#1d1d1f")
muted = colors.HexColor("#52514e")
accent = colors.HexColor("#0066cc")
border = colors.HexColor("#d6d6d6")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=26, textColor=ink, spaceAfter=2)
date_style = ParagraphStyle("DateLine", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=13, textColor=muted, spaceAfter=4)
daytype_style = ParagraphStyle("DayType", parent=styles["Normal"], fontName="Helvetica-Bold",
                                fontSize=13, textColor=accent, spaceAfter=10)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                     fontSize=14, textColor=ink, spaceBefore=14, spaceAfter=6)
body = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica",
                       fontSize=11, textColor=ink, leading=15)
meal_item = ParagraphStyle("MealItem", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=11, textColor=ink, leading=15, leftIndent=0)
macro_line = ParagraphStyle("MacroLine", parent=styles["Normal"], fontName="Helvetica-Bold",
                             fontSize=10.5, textColor=muted, spaceBefore=4)
rule_item = ParagraphStyle("Rule", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=10.5, textColor=muted, leading=14)

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
)

story = []
story.append(Paragraph("Zielgerade — Tagesplan", title_style))
story.append(Paragraph(DATE_STR, date_style))
story.append(Paragraph(DAY_TYPE, daytype_style))

target_tbl = Table(
    [["Protein", "Fett", "Kohlenhydrate", "≈ kcal"],
     [f"{TARGET_P}g", f"{TARGET_F}g", f"{TARGET_C}g", f"{TARGET_KCAL}"]],
    colWidths=[40 * mm] * 4,
)
target_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5f5f7")),
    ("TEXTCOLOR", (0, 0), (-1, 0), muted),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 11),
    ("TEXTCOLOR", (0, 1), (-1, 1), ink),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BOX", (0, 0), (-1, -1), 0.75, border),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, border),
    ("TOPPADDING", (0, 0), (-1, -1), 8),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
story.append(target_tbl)
story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))

for meal in MEALS:
    story.append(Paragraph(meal["name"], h2))
    for item in meal["items"]:
        story.append(Paragraph(f"•  {item}", meal_item))
    story.append(Paragraph(
        f"≈ {meal['p']}g P / {meal['f']}g F / {meal['c']}g C", macro_line
    ))

story.append(Spacer(1, 6 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))
story.append(Paragraph("Feste Regeln", h2))
for r in RULES:
    story.append(Paragraph(f"•  {r}", rule_item))

doc.build(story)
print("done:", OUT_PATH)

"""
Generates the fixed 2-week routine sheet (same meals every day) to fix
midnight hunger attacks: bigger, protein+fat-forward dinner, slightly
higher daily kcal than the Kickstart baseline.
Usage: run as-is; edit CONFIG only if the routine itself changes.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

# ---------------- CONFIG ----------------
OUT_PATH = "/home/user/Metabolic/scripts/routine_2wochen.pdf"
START_STR = "ab Donnerstag, 27. November 2026 — 2 Wochen fix"
TARGET_P, TARGET_F, TARGET_C, TARGET_KCAL = 200, 65, 140, 1950

MEALS = [
    {
        "name": "Frühstück (immer gleich)",
        "items": ["450g Magerquark", "150g TK-Beeren (aufgetaut)", "25g Walnüsse"],
        "p": 60, "f": 20, "c": 35,
    },
    {
        "name": "Mittag (immer gleich)",
        "items": ["250g Hähnchenbrust", "Großer Salat (beliebige Menge)",
                   "100g Reis (gekocht)", "1 EL Olivenöl"],
        "p": 85, "f": 20, "c": 60,
    },
    {
        "name": "Abend (immer gleich, vor 21 Uhr — bewusst größer gegen Nachthunger)",
        "items": ["250g Garnelen oder Lachs (frei abwechselnd)", "300g gedünstetes Gemüse (TK)",
                   "100g Kartoffeln", "1 EL Olivenöl"],
        "p": 55, "f": 25, "c": 45,
    },
]

PREP_TIPS = [
    "So/Mi: 500-750g Hähnchenbrust + Reis auf Vorrat kochen, portionsweise im Kühlschrank (3-4 Tage haltbar)",
    "Garnelen/Lachs: nur 5-8 Min. frisch anbraten, kein Vorkochen nötig",
    "Gemüse: TK-Dampfgemüse im Beutel, 5 Min. Mikrowelle",
    "Beeren: TK, kein Schneiden, einfach auftauen",
]

SOS_TIPS = [
    "Erst ein großes Glas Wasser oder Tee, nicht gleich essen",
    "Passiert es öfter als 1x/Woche: Rückmeldung geben — dann wird das Abendessen nochmal vergrößert, kein Snack nebenbei",
]

SHOPPING_LIST = [
    "Magerquark: ~3,2 kg (6-7 Becher à 500g)",
    "TK-Beeren: ~1 kg",
    "Walnüsse: 1 Packung (175-200g)",
    "Hähnchenbrust: 1,75 kg",
    "Salat: 2-3 Köpfe oder Beutelsalat nach Bedarf",
    "Reis (roh): 1 kleine Packung (~250g reichen für die Woche)",
    "Garnelen und/oder Lachs: 1,75 kg insgesamt (frei aufteilen)",
    "TK-Gemüse: ~2,1 kg (z.B. 3 Beutel à 750g)",
    "Kartoffeln: 700g",
    "Olivenöl: vorhandene Flasche reicht meist (~210ml/Woche)",
]

RULES = [
    "3 Mahlzeiten/Tag, mind. 5h Pause dazwischen",
    "Mit 1-2 Bissen Eiweiß beginnen",
    "Pro Mahlzeit nur eine Eiweißart",
    "Nichts nach 21 Uhr",
    "3,4L Wasser über den Tag (erstes Glas direkt nach dem Aufstehen)",
    "Kein Alkohol",
]
# -----------------------------------------

ink = colors.HexColor("#1d1d1f")
muted = colors.HexColor("#52514e")
accent = colors.HexColor("#0066cc")
border = colors.HexColor("#d6d6d6")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=26, textColor=ink, spaceAfter=2)
date_style = ParagraphStyle("DateLine", parent=styles["Normal"], fontName="Helvetica",
                             fontSize=13, textColor=muted, spaceAfter=10)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                     fontSize=14, textColor=ink, spaceBefore=14, spaceAfter=6)
body = ParagraphStyle("Body", parent=styles["Normal"], fontName="Helvetica",
                       fontSize=11, textColor=ink, leading=15)
meal_item = ParagraphStyle("MealItem", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=11, textColor=ink, leading=15)
macro_line = ParagraphStyle("MacroLine", parent=styles["Normal"], fontName="Helvetica-Bold",
                             fontSize=10.5, textColor=muted, spaceBefore=4)
rule_item = ParagraphStyle("Rule", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=10.5, textColor=muted, leading=14)

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
)

story = []
story.append(Paragraph("Zielgerade — Fix-Routine gegen Nachthunger", title_style))
story.append(Paragraph(START_STR, date_style))

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

story.append(Paragraph("Täglicher Plan — 14 Tage exakt gleich", h2))
for meal in MEALS:
    story.append(Paragraph(meal["name"], ParagraphStyle(
        "MealName", parent=body, fontName="Helvetica-Bold", textColor=accent, spaceBefore=8)))
    for item in meal["items"]:
        story.append(Paragraph(f"•  {item}", meal_item))
    story.append(Paragraph(
        f"≈ {meal['p']}g P / {meal['f']}g F / {meal['c']}g C", macro_line
    ))

story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))
story.append(Paragraph("Prep-Tipps", h2))
for t in PREP_TIPS:
    story.append(Paragraph(f"•  {t}", rule_item))

story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))
story.append(Paragraph("SOS bei Hunger nachts", h2))
for t in SOS_TIPS:
    story.append(Paragraph(f"•  {t}", rule_item))

story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))
story.append(Paragraph("Einkaufsliste pro Woche (2x kaufen für 2 Wochen)", h2))
for item in SHOPPING_LIST:
    story.append(Paragraph(f"•  {item}", rule_item))

story.append(Spacer(1, 4 * mm))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))
story.append(Paragraph("Feste Regeln", h2))
for r in RULES:
    story.append(Paragraph(f"•  {r}", rule_item))

doc.build(story)
print("done:", OUT_PATH)

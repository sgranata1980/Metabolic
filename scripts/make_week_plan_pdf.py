"""
Generates the weekly A4 meal-plan + shopping-list sheet for the Kickstart phase.
Run once per week, update WEEK_LABEL for the date range.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)

OUT_PATH = "/home/user/Metabolic/scripts/wochenplan.pdf"
WEEK_LABEL = "Woche ab Montag, 23. November 2026 — Restart"

DAYS = [
    ("Montag", "Lockerer Lauf", "190/60/90",
     "450g Magerquark, 100g Beeren, 20g Walnüsse",
     "300g Hähnchenbrust, großer Salat, 50g Avocado, 1 TL Olivenöl",
     "300g Kabeljau, 200g Gemüse, 60g Süßkartoffel, 1 EL Olivenöl"),
    ("Dienstag", "Intervalle", "190/60/90",
     "4 Eier + 2 Eiklar, 150g Spinat, 40g Haferflocken",
     "220g Putenbrust, großer Salat, 50g Avocado, 1 TL Olivenöl",
     "250g Hähnchenbrust, 250g Gemüse, 80g Quinoa, 1 EL Olivenöl"),
    ("Mittwoch", "Lockerer Lauf", "190/60/90",
     "300g Skyr, 1 Banane, 15g Mandeln",
     "250g mageres Rinderhack, großer Salat, 80g Kichererbsen",
     "250g Kabeljau, 200g Gemüse, 60g Süßkartoffel, 1 EL Olivenöl"),
    ("Donnerstag", "Lockerer Lauf", "190/60/90",
     "450g Magerquark, 100g Beeren, 20g Walnüsse",
     "250g Hähnchenbrust, großer Salat, 50g Avocado, 1 TL Olivenöl",
     "250g Garnelen, 250g Gemüse, 60g Vollkornreis, 1 EL Olivenöl"),
    ("Freitag", "Krafttag", "190/60/90",
     "4 Eier + 2 Eiklar, 150g Spinat, 40g Haferflocken",
     "220g Putenbrust, großer Salat, 50g Avocado, 1 TL Olivenöl",
     "250g Hähnchenbrust, 250g Gemüse, 80g Quinoa, 1 EL Olivenöl"),
    ("Samstag", "Krafttag", "190/60/90",
     "300g Skyr, 1 Banane, 15g Mandeln",
     "250g Garnelen, großer Salat, 60g Vollkornreis, 1 EL Olivenöl",
     "220g Lachs, 200g Spargel/Zucchini, 50g Kartoffeln"),
    ("Sonntag", "Long Run", "190/60/140",
     "400g Magerquark, 150g Beeren, 40g Haferflocken, 10g Honig",
     "250g mageres Rinderhack, großer Salat, 80g Kichererbsen",
     "220g Putenbrust, 250g Gemüse, 100g Süßkartoffel"),
]

SHOPPING_LIST = [
    ("Fleisch / Fisch", [
        "Hähnchenbrust — 1.050g",
        "Putenbrust — 440g",
        "Mageres Rinderhack — 500g",
        "Kabeljau — 550g",
        "Garnelen — 500g",
        "Lachs — 220g",
    ]),
    ("Milchprodukte / Eier", [
        "Magerquark — ca. 1,3kg",
        "Skyr — 600g",
        "Eier — 1 Packung (10er, für 2x \"4 Eier+2 Eiklar\")",
    ]),
    ("Gemüse / Salat", [
        "Gemischter Salat (Rucola/Tomate/Gurke/Paprika/Blattsalat) — ca. 1,5kg",
        "Brokkoli/Zucchini-Mix — ca. 1,4kg",
        "Spinat — 300g",
        "Spargel oder Zucchini (für Samstag) — 200g",
        "Avocado — 2 Stück",
    ]),
    ("Kohlenhydrate / Sonstiges", [
        "Haferflocken — 125g",
        "Vollkornreis — 120g",
        "Quinoa — 160g",
        "Süßkartoffel — 160g",
        "Kartoffeln — 50g",
        "Kichererbsen (Dose) — 1 Dose",
        "Beeren (Himbeeren/Heidelbeeren, TK geht auch) — 350g",
        "Walnüsse — 40g",
        "Mandeln — 30g",
        "Banane — 2 Stück",
        "Honig — 1 kleines Glas (Rest reicht lange)",
        "Olivenöl — 1 Flasche (falls nicht vorhanden)",
    ]),
]

ink = colors.HexColor("#1d1d1f")
muted = colors.HexColor("#52514e")
accent = colors.HexColor("#0066cc")
border = colors.HexColor("#d6d6d6")
header_bg = colors.HexColor("#f5f5f7")

styles = getSampleStyleSheet()
title_style = ParagraphStyle("TitleBig", parent=styles["Title"], fontName="Helvetica-Bold",
                              fontSize=24, textColor=ink, spaceAfter=2)
sub_style = ParagraphStyle("Sub", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=12, textColor=muted, spaceAfter=10)
h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                     fontSize=14, textColor=ink, spaceBefore=10, spaceAfter=6)
cell_day = ParagraphStyle("CellDay", parent=styles["Normal"], fontName="Helvetica-Bold",
                           fontSize=10, textColor=ink, leading=12)
cell_type = ParagraphStyle("CellType", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=8.5, textColor=accent, leading=11)
cell_body = ParagraphStyle("CellBody", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=8.5, textColor=ink, leading=11)
list_item = ParagraphStyle("ListItem", parent=styles["Normal"], fontName="Helvetica",
                            fontSize=10.5, textColor=ink, leading=15)
cat_header = ParagraphStyle("CatHeader", parent=styles["Normal"], fontName="Helvetica-Bold",
                             fontSize=12, textColor=accent, spaceBefore=10, spaceAfter=4)

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    leftMargin=16 * mm, rightMargin=16 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
)

story = []
story.append(Paragraph("Zielgerade — Wochenplan", title_style))
story.append(Paragraph(WEEK_LABEL, sub_style))

header_row = [
    Paragraph("Tag", cell_day), Paragraph("Ziel P/F/C", cell_day),
    Paragraph("Frühstück", cell_day), Paragraph("Mittag", cell_day), Paragraph("Abend", cell_day),
]
rows = [header_row]
for day, typ, macros, b, l, d in DAYS:
    rows.append([
        Paragraph(f"{day}<br/><font color='#0066cc'>{typ}</font>", cell_day),
        Paragraph(macros, cell_body),
        Paragraph(b, cell_body),
        Paragraph(l, cell_body),
        Paragraph(d, cell_body),
    ])

col_widths = [24 * mm, 20 * mm, 43 * mm, 43 * mm, 48 * mm]
week_tbl = Table(rows, colWidths=col_widths, repeatRows=1)
week_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), header_bg),
    ("BOX", (0, 0), (-1, -1), 0.75, border),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, border),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
]))
story.append(week_tbl)

story.append(PageBreak())
story.append(Paragraph("Einkaufsliste", title_style))
story.append(Paragraph(WEEK_LABEL, sub_style))
story.append(HRFlowable(width="100%", thickness=0.75, color=border))

for category, items in SHOPPING_LIST:
    story.append(Paragraph(category, cat_header))
    for item in items:
        story.append(Paragraph(f"☐  {item}", list_item))

doc.build(story)
print("done:", OUT_PATH)

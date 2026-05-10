"""
Script to generate a blank 'pdf form.pdf' template that preserves
the exact layout of the original but with empty spaces for dynamic data.
Run this once to regenerate the template.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm, mm

OUTPUT_PATH = "A:/stagio/PROJECT_LSN/Back-end/pdf form.pdf"

W, H = A4  # 595.27 x 841.89 points

c = canvas.Canvas(OUTPUT_PATH, pagesize=A4)

# ─── HEADER ────────────────────────────────────────────────────────────
# Arabic header line (simulated with latin placeholder since reportlab doesn't render RTL by default)
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.2, 0.2, 0.2)
c.drawCentredString(W / 2, H - 30, "الجمهورية الجزائرية الديمقراطية الشعبية  ·  الجمهورية الجزائرية الديمقراطية الشعبية")

c.setFont("Helvetica", 8.5)
c.drawCentredString(W / 2, H - 45, "République Algérienne Démocratique et Populaire")
c.drawCentredString(W / 2, H - 57, "Ministère de l'Enseignement Supérieur et de la Recherche Scientifique")

c.setFont("Helvetica-Bold", 10)
c.drawCentredString(W / 2, H - 73, "University Constantine 1 Mentouri")

c.setFont("Helvetica", 8.5)
c.drawCentredString(W / 2, H - 86, "Internship Office — Service des Stages")

# Divider line
c.setStrokeColorRGB(0.2, 0.2, 0.2)
c.setLineWidth(1)
c.line(40, H - 94, W - 40, H - 94)

# ─── REF + ACADEMIC YEAR ──────────────────────────────────────────────
c.setFont("Helvetica", 8)
c.setFillColorRGB(0, 0, 0)
c.drawString(40, H - 107, "Réf N° : ___________")
c.drawRightString(W - 40, H - 107, "Academic Year : ___________")

# ─── MAIN TITLE ───────────────────────────────────────────────────────
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(W / 2, H - 135, "CONVENTION DE STAGE")
c.setFont("Helvetica", 13)
c.setFillColorRGB(0.4, 0.4, 0.4)
c.drawCentredString(W / 2, H - 153, "Internship Agreement")
c.setFillColorRGB(0, 0, 0)

# Thin divider
c.setLineWidth(0.5)
c.line(80, H - 162, W - 80, H - 162)

# ─── UNIVERSITY SECTION ───────────────────────────────────────────────
y = H - 178
c.setFont("Helvetica-Bold", 9)
c.drawString(40, y, "University Institution / Établissement d'enseignement")

c.setFont("Helvetica", 9)
fields = [
    ("Name:", "University Constantine 1 Mentouri"),
    ("Address:", ", 25 - Constantine"),
    ("Represented by:", "University Administrator"),
    ("Department:", "Internship Office"),
    ("Email:", "admin@univ-constantine1.dz"),
]
y -= 14
for label, value in fields:
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(50, y, label)
    c.setFont("Helvetica", 8.5)
    c.drawString(140, y, value)
    y -= 13

# BETWEEN separator
c.setFont("Helvetica-Bold", 12)
c.setFillColorRGB(0.8, 0.1, 0.1)
c.drawCentredString(W / 2, y - 4, "BETWEEN")
c.setFillColorRGB(0, 0, 0)
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(W / 2, y - 18, "&")
c.setFont("Helvetica-Bold", 12)
c.setFillColorRGB(0.8, 0.1, 0.1)
c.drawCentredString(W / 2, y - 32, "ET")
c.setFillColorRGB(0, 0, 0)
y -= 48

# ─── COMPANY SECTION ──────────────────────────────────────────────────
c.setFont("Helvetica-Bold", 9)
c.drawString(40, y, "Host Organisation / Établissement d'accueil")
y -= 14
for label in [("Name:", ""), ("Wilaya:", ""), ("Website:", ""), ("Email:", "")]:
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(50, y, label[0])
    # Draw underline for the blank field
    c.setLineWidth(0.4)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(140, y - 2, W - 50, y - 2)
    c.setStrokeColorRGB(0, 0, 0)
    y -= 13

# ─── STUDENT SECTION ──────────────────────────────────────────────────
y -= 6
c.setFont("Helvetica-Bold", 9)
c.setFillColorRGB(0.1, 0.1, 0.5)
c.drawString(40, y, "STUDENT INFORMATION / DONNÉES RELATIVES À L'ÉTUDIANT")
c.setFillColorRGB(0, 0, 0)
y -= 14
for label in [("Full Name:", ""), ("Email:", ""), ("Wilaya:", ""), ("University:", ""), ("GitHub:", ""), ("Portfolio:", "")]:
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(50, y, label[0])
    c.setLineWidth(0.4)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(140, y - 2, W - 50, y - 2)
    c.setStrokeColorRGB(0, 0, 0)
    y -= 13

# ─── INTERNSHIP SUBJECT & DESCRIPTION ────────────────────────────────
y -= 6
c.setFont("Helvetica-Bold", 8.5)
c.drawString(40, y, "Internship Subject:")
c.setLineWidth(0.4)
c.setStrokeColorRGB(0.5, 0.5, 0.5)
c.line(140, y - 2, W - 50, y - 2)
c.setStrokeColorRGB(0, 0, 0)
y -= 13

c.setFont("Helvetica-Bold", 8.5)
c.drawString(40, y, "Description:")
# Multi-line blank area
for _ in range(3):
    y -= 13
    c.setLineWidth(0.4)
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.line(50, y - 2, W - 50, y - 2)
    c.setStrokeColorRGB(0, 0, 0)

# ─── DURATION ROW ─────────────────────────────────────────────────────
y -= 16
# Draw three boxes side by side
box_y = y
box_h = 32
box_labels = ["DURATION", "START DATE", "END DATE"]
box_widths = [170, 160, 165]
box_x = 40
c.setFont("Helvetica-Bold", 8)
for i, (label, bw) in enumerate(zip(box_labels, box_widths)):
    # Box border
    c.setStrokeColorRGB(0.3, 0.3, 0.3)
    c.setLineWidth(0.5)
    c.rect(box_x, box_y - box_h, bw, box_h)
    # Label at top of box
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(box_x + 4, box_y - 10, label)
    # Blank value line
    c.setStrokeColorRGB(0.5, 0.5, 0.5)
    c.setLineWidth(0.3)
    c.line(box_x + 4, box_y - 26, box_x + bw - 8, box_y - 26)
    box_x += bw + 2
c.setFillColorRGB(0, 0, 0)

# ─── FOOTER / PAGE MARKER ─────────────────────────────────────────────
y = box_y - box_h - 20
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawString(40, y, "Convention de Stage — Réf: ___________  A.Y. ___________")
c.drawRightString(W - 40, y, ", 25 - Constantine    Page 1 / 3")
c.setFillColorRGB(0, 0, 0)

# Bottom horizontal line
c.setStrokeColorRGB(0.2, 0.2, 0.2)
c.setLineWidth(1)
c.line(40, y - 8, W - 40, y - 8)

c.showPage()

# ─── PAGE 2 (signatures page) ─────────────────────────────────────────
c.setFont("Helvetica-Bold", 10)
c.drawCentredString(W / 2, H - 80, "Signatures / التوقيعات")

sig_y = H - 180
sig_labels = ["The University\nL'Université", "The Host Organisation\nL'Entreprise d'accueil"]
sig_x_positions = [70, 340]
sig_w, sig_h = 180, 100

for label, sx in zip(sig_labels, sig_x_positions):
    c.setFont("Helvetica-Bold", 9)
    for i, line in enumerate(label.split("\n")):
        c.drawString(sx, sig_y + sig_h + 12 - i * 12, line)
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setLineWidth(0.5)
    c.rect(sx, sig_y, sig_w, sig_h)
    c.setFont("Helvetica", 7)
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.drawString(sx + 4, sig_y + 4, "Signature & Stamp / Cachet et Signature")
    c.setFillColorRGB(0, 0, 0)

c.setFont("Helvetica", 7)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawCentredString(W / 2, 30, "Convention de Stage — Stag.io    Page 2 / 3")
c.setFillColorRGB(0, 0, 0)
c.showPage()

# ─── PAGE 3 (student signature) ───────────────────────────────────────
c.setFont("Helvetica-Bold", 10)
c.drawCentredString(W / 2, H - 80, "Student Acknowledgement / Accord de l'Étudiant")

c.setFont("Helvetica", 9)
c.drawString(70, H - 160, "I, the undersigned, confirm that I have read and agree to the terms of this internship agreement.")
c.drawString(70, H - 175, "Je soussigné(e) confirme avoir lu et accepté les termes de la présente convention.")

sig_y2 = H - 340
c.setFont("Helvetica-Bold", 9)
c.drawString(70, sig_y2 + 112, "Student / L'Étudiant(e)")
c.setStrokeColorRGB(0.4, 0.4, 0.4)
c.setLineWidth(0.5)
c.rect(70, sig_y2, 180, 100)
c.setFont("Helvetica", 7)
c.setFillColorRGB(0.6, 0.6, 0.6)
c.drawString(74, sig_y2 + 4, "Signature")
c.setFillColorRGB(0, 0, 0)

c.setFont("Helvetica", 7)
c.setFillColorRGB(0.5, 0.5, 0.5)
c.drawCentredString(W / 2, 30, "Convention de Stage — Stag.io    Page 3 / 3")
c.setFillColorRGB(0, 0, 0)
c.showPage()

c.save()
print(f"Template saved to {OUTPUT_PATH}")

import os
import io
import textwrap
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
from core.models import InternshipAgreement


def _white(can, x, y, w, h):
    """Draw a white rectangle to cover old text."""
    can.setFillColorRGB(1, 1, 1)
    can.rect(x, y, w, h, fill=1, stroke=0)
    can.setFillColorRGB(0, 0, 0)


def generate_internship_agreement(internship, admin=None):
    """
    Generate a PDF by overlaying dynamic data onto the PDF template.
    White rectangles first erase the old dummy data, then the real data is drawn.
    """
    filename = f'agreement_{internship.id}.pdf'
    filepath = os.path.join(settings.MEDIA_ROOT, 'agreements', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    template_path = os.path.join(settings.BASE_DIR.parent, '81eea5ce-25ab-47a9-9443-9c46560ccac2.pdf')
    if not os.path.exists(template_path):
        raise ValueError("The template PDF was not found in the Back-end directory.")

    W, H = A4  # 595.27 x 841.89

    # ── Gather data ──────────────────────────────────────────────────────────
    ref_no       = f'CS-{internship.id}/{internship.created_at.year}'
    academic_year = f'{internship.created_at.year - 1}/{internship.created_at.year}'
    comp_name    = internship.company.name
    comp_wilaya  = internship.company.wilaya
    comp_email   = internship.company.email
    stu_name     = internship.student.full_name
    stu_email    = internship.student.email
    stu_wilaya   = internship.student.wilaya
    stu_univ     = internship.student.university.name if internship.student.university else "N/A"
    stu_cv       = getattr(internship.student, 'cv', None)
    github       = getattr(stu_cv, 'github', '') or ''
    portfolio    = getattr(stu_cv, 'portfolio', '') or ''
    subject      = internship.subject or ''
    description  = internship.description or ''
    if internship.offer and internship.offer.start_date and internship.offer.end_date:
        from datetime import date
        delta = internship.offer.end_date - internship.offer.start_date
        months = round(delta.days / 30)
        duration = f"{months} month(s)"
    else:
        duration = "N/A"
    start_date   = internship.start_date.strftime('%d %b %Y') if internship.start_date else 'N/A'
    end_date     = internship.end_date.strftime('%d %b %Y') if internship.end_date else 'N/A'
    admin_univ   = admin.university.name if admin and admin.university else stu_univ

    # ── Page 1 overlay ───────────────────────────────────────────────────────
    p1 = io.BytesIO()
    c1 = canvas.Canvas(p1, pagesize=A4)
    c1.setFont("Helvetica", 9)

    def wipe_and_write(can, x_label_end, y, text, max_width=340, font="Helvetica", size=9):
        """Erase old value and write new one starting just after the label."""
        can.setFont(font, size)
        # White rectangle covers old value region
        _white(can, x_label_end - 2, y - 3, max_width, 12)
        can.drawString(x_label_end, y, str(text))

    # ── Header sidebar (running footer on right) ──────────────────────────────
    # Erase all old sidebar text (university name, ref, a.y.) in the right column
    # These are at x0=232-375, y=796-820 — just erase that zone
    _white(c1, 231, 793, 150, 32)   # covers "University / Constantine 1 / Mentouri" sidebar
    _white(c1, 280, 793, 100, 32)   # covers "Convention de Stage / ref / a.y." sidebar
    _white(c1, 338, 793, 40, 32)    # covers "A.Y." and year

    # ── Ref N° and Academic Year (y≈670) ─────────────────────────────────────
    # Old: 'Réf N° : CS-4/2026' at x0=56.7, y=670.1
    _white(c1, 56, 668, 200, 12)
    c1.setFont("Helvetica", 9)
    c1.drawString(56.7, 670, f"Réf N° : {ref_no}")

    # Old: 'Academic Year : 2025/2026' at x0=444.2, y=670.1
    _white(c1, 444, 668, 100, 12)
    c1.drawString(444.2, 670, f"Academic Year : {academic_year}")

    # ── University name in header (y≈718) ─────────────────────────────────────
    # Old 'UniversityConstantine1Mentouri' at y=718.9
    _white(c1, 215, 716, 200, 14)
    c1.setFont("Helvetica-Bold", 11)
    c1.drawString(216.6, 718.9, admin_univ)

    # ── Company section (y≈529) ───────────────────────────────────────────────
    # Name: old 'Cyber-Comp' at x0=388.9, y=529.1
    _white(c1, 388, 526, 180, 12)
    c1.setFont("Helvetica", 9)
    c1.drawString(388.9, 529.1, comp_name)

    # Wilaya: old 'Constantine' at x0=388.9, y=513.0
    _white(c1, 388, 510, 180, 12)
    c1.drawString(388.9, 513.0, comp_wilaya)

    # Website: row at y≈497 — nothing to erase (was blank in original)

    # Email: old 'Cyber-Comp@gmail.com' at x0=388.9, y=480.8
    _white(c1, 388, 477, 180, 12)
    c1.drawString(388.9, 480.8, comp_email)

    # ── Student section (y≈414 down) ──────────────────────────────────────────
    # Full Name: old 'AdelChibi' at x0=146.7, y=414.2
    _white(c1, 146, 411, 360, 12)
    c1.drawString(146.7, 414.2, stu_name)

    # Email: old 'AdelChibi@univ-constantine1.dz' at x0=146.7, y=399.8
    _white(c1, 146, 396, 360, 12)
    c1.drawString(146.7, 399.8, stu_email)

    # Wilaya: old '25 - Constantine' at x0=146.7, y=385.4
    _white(c1, 146, 382, 360, 12)
    c1.drawString(146.7, 385.4, stu_wilaya)

    # University: old 'University Constantine 1 Mentouri' at x0=146.7, y=371.0
    _white(c1, 146, 368, 360, 12)
    c1.drawString(146.7, 371.0, stu_univ)

    # GitHub: old 'https://github.com/' at x0=146.7, y=349.1
    _white(c1, 146, 346, 360, 12)
    c1.drawString(146.7, 349.1, github)

    # Portfolio: old long URL at x0=146.7, y=334.7
    _white(c1, 146, 331, 360, 12)
    c1.setFont("Helvetica", 7.5)
    c1.drawString(146.7, 334.7, portfolio[:90])
    c1.setFont("Helvetica", 9)

    # ── Internship Subject: old 'Hi' at x0=146.7, y=320.3 ────────────────────
    _white(c1, 146, 317, 360, 12)
    c1.drawString(146.7, 320.3, subject)

    # ── Description: old 'Nice to meet u' at x0=146.7, y=305.9 ───────────────
    _white(c1, 146, 290, 370, 25)  # wipe enough space for multi-line
    desc_lines = textwrap.wrap(description, width=80)
    for i, line in enumerate(desc_lines[:2]):
        c1.drawString(146.7, 305.9 - (i * 14), line)

    # ── Duration / Start / End at y≈263.8 ─────────────────────────────────────
    # Duration: old '1 month and 1 day' at x0=64.9, y=263.8
    _white(c1, 64, 260, 155, 12)
    c1.setFont("Helvetica-Bold", 9)
    c1.drawString(64.9, 263.8, duration)

    # Start Date: old '01 Jul 2026' at x0=225.1, y=263.8
    _white(c1, 225, 260, 155, 12)
    c1.drawString(225.1, 263.8, start_date)

    # End Date: old '01 Aug 2026' at x0=385.2, y=263.8
    _white(c1, 385, 260, 155, 12)
    c1.drawString(385.2, 263.8, end_date)

    c1.save()

    # ── Page 2 overlay: replace inline references to student/company ──────────
    p2 = io.BytesIO()
    c2 = canvas.Canvas(p2, pagesize=A4)
    c2.setFont("Helvetica", 9)

    # Article 2 mentions student + company at y≈651.5
    # "carried out by AdelChibi at Cyber-Comp" — wipe the names inline
    # We wipe a wide band and rewrite the full sentence
    _white(c2, 56, 648, 490, 13)
    c2.setFont("Helvetica", 9)
    c2.drawString(56.7, 651.5, f"This convention defines the organisational framework for the practical internship carried out by {stu_name} at {comp_name},")

    # Article 3 internship subject at y≈580.2 — "The internship subject is: Hi."
    _white(c2, 56, 577, 490, 13)
    c2.drawString(56.7, 580.2, f"professional competencies, and prepare for working life. The internship subject is: {subject}.")

    # Article 5 — University name at y≈451
    _white(c2, 70, 448, 460, 13)
    c2.drawString(70.2, 451.0, f"An Academic Supervisor designated by {admin_univ}, responsible for pedagogical follow-up and")

    # Article 5 — company at y≈421
    _white(c2, 70, 418, 460, 13)
    c2.drawString(70.2, 421.0, f"A Host Supervisor designated by {comp_name}, responsible for daily on-site supervision.")

    # Article 6 — Duration / dates at y≈348.4
    _white(c2, 70, 345, 460, 13)
    c2.drawString(70.2, 348.4, f"Duration: {duration} — from {start_date} to {end_date}.")

    # Article 6 — academic year at y≈332.6
    _white(c2, 70, 329, 460, 13)
    c2.drawString(70.2, 332.6, f"The internship is carried out during academic year {academic_year}.")

    # Article 7 — university names at y≈292 and 277 and 261
    for y_line, old_text in [(292.2, None), (277.0, None), (261.8, None)]:
        _white(c2, 56, y_line - 3, 490, 13)
    c2.setFont("Helvetica", 9)
    c2.drawString(56.7, 292.2, f"The student retains their registered student status throughout the internship. Social security coverage is provided by {admin_univ}.")
    c2.drawString(56.7, 277.0, f"In the event of a work-related accident, the host institution must file the workplace accident declaration")
    c2.drawString(56.7, 261.8, f"with the relevant social security body and send a copy to {admin_univ} without delay.")

    # Article 9 — university + company at y≈149.6
    _white(c2, 56, 146, 490, 13)
    c2.drawString(56.7, 149.6, f"Work results are the joint property of {admin_univ} and {comp_name}. The internship report must be")

    c2.save()

    # ── Page 3 overlay: signature names ──────────────────────────────────────
    p3 = io.BytesIO()
    c3 = canvas.Canvas(p3, pagesize=A4)
    c3.setFont("Helvetica", 9)

    # Article 12 dates at y≈693.2
    _white(c3, 56, 690, 490, 13)
    c3.drawString(56.7, 693.2, f"This convention is valid solely from {start_date} to {end_date} and enters into force upon signature by all parties.")

    # "Done at" date at y≈656.1
    _white(c3, 56, 653, 250, 13)
    from datetime import date
    today = date.today().strftime("%d %b %Y")
    c3.drawString(56.7, 656.1, f"Done at 25-Constantine, on {today}")

    # ── Signature block — only replace the dynamic name/email fields ───────────
    # Company name: 'Cyber-Comp' at x0=275.7, y=601.0
    _white(c3, 275, 598, 110, 13)
    c3.drawString(275.7, 601.0, comp_name[:18])

    # Company wilaya: 'Constantine' at x0=277.8, y=585.9
    _white(c3, 277, 582, 110, 13)
    c3.drawString(277.8, 585.9, comp_wilaya)

    # Student name: 'AdelChibi' at x0=440.7, y=601.0
    _white(c3, 440, 598, 110, 13)
    c3.drawString(440.7, 601.0, stu_name[:15])

    # Student email: at x0=402.6, y=585.9
    _white(c3, 402, 582, 145, 13)
    c3.setFont("Helvetica", 7)
    c3.drawString(402.6, 585.9, stu_email[:35])
    c3.setFont("Helvetica", 9)

    c3.save()

    # ── Merge all overlays onto the template ──────────────────────────────────
    template_pdf = PdfReader(template_path)
    output = PdfWriter()

    overlays = [p1, p2, p3]
    for i, overlay_buf in enumerate(overlays):
        overlay_buf.seek(0)
        overlay_pdf = PdfReader(overlay_buf)
        page = template_pdf.pages[i]
        page.merge_page(overlay_pdf.pages[0])
        output.add_page(page)

    with open(filepath, "wb") as out_stream:
        output.write(out_stream)

    # Save to model
    from django.core.files import File
    with open(filepath, 'rb') as f:
        agreement, _ = InternshipAgreement.objects.get_or_create(internship=internship)
        agreement.pdf_file.save(filename, File(f), save=True)

    return agreement

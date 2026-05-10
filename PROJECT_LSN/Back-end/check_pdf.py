import os
import sys
from PyPDF2 import PdfReader

pdf_path = "A:/stagio/PROJECT_LSN/Back-end/pdf form.pdf"

if not os.path.exists(pdf_path):
    print("PDF not found!")
    sys.exit(1)

reader = PdfReader(pdf_path)
fields = reader.get_fields()

if fields:
    print("PDF has form fields:")
    for key in fields.keys():
        print(f"- {key}")
else:
    print("PDF does not have form fields.")

page = reader.pages[0]
text = page.extract_text()
with open("A:/stagio/PROJECT_LSN/Back-end/pdf_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("Text extracted to pdf_text.txt")

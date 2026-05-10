"""Extract text with X/Y coordinates from the PDF template to map field positions."""
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar

pdf_path = "A:/stagio/PROJECT_LSN/Back-end/81eea5ce-25ab-47a9-9443-9c46560ccac2.pdf"

with open("A:/stagio/PROJECT_LSN/Back-end/coords_clean.txt", "w", encoding="utf-8") as out:
    for page_num, page_layout in enumerate(extract_pages(pdf_path)):
        out.write(f"\n=== PAGE {page_num + 1} (height={page_layout.height:.1f}) ===\n")
        items = []
        for element in page_layout:
            if isinstance(element, LTTextBox):
                for line in element:
                    if isinstance(line, LTTextLine):
                        text = line.get_text().strip()
                        if text:
                            items.append((line.y0, line.x0, line.x1, text))
        for y0, x0, x1, text in sorted(items, key=lambda r: -r[0]):
            out.write(f"  y={y0:6.1f}  x0={x0:6.1f}  x1={x1:6.1f}  '{text}'\n")
print("Done")

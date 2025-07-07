import os
from fpdf import FPDF

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def save_as_txt(entry_id, summary, resources):
    path = os.path.join(EXPORT_DIR, f"{entry_id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("Summary:\n")
        f.write(summary + "\n\nResources:\n")
        f.write(resources)
    return path

def save_as_pdf(entry_id, summary, resources):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)   # ✅ Built-in font

    # Clean text: remove fancy Unicode chars that break Latin-1
    def safe_text(s):
        return s.encode('latin-1', 'ignore').decode('latin-1')

    pdf.multi_cell(0, 10, safe_text("Summary:\n" + summary))
    pdf.ln(10)
    pdf.multi_cell(0, 10, safe_text("Resources:\n" + resources))

    path = os.path.join(EXPORT_DIR, f"{entry_id}.pdf")
    pdf.output(path)
    return path

import pdfplumber
def pdf_to_text(file):
    with pdfplumber.open(file) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)
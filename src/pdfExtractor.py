import pdfplumber

def extract_pdf_text(filename):
    with pdfplumber.open(filename) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text
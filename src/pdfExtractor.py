import pdfplumber

def extractPdfText(filename):
    with pdfplumber.open(filename) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text()
    return all_text
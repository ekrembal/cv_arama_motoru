from PyPDF2 import PdfFileReader
import re

def get_text_from_pdf(filepath):
    pdf = PdfFileReader(open(filepath, "rb"))
    text = ''
    for page in pdf.pages:
        text += page.extractText()
    text = re.sub(r'\s+', '', text)
    return text.lower()

if __name__ == '__main__':
    print(get_text_from_pdf('cv_ler/bos-cv.pdf'))
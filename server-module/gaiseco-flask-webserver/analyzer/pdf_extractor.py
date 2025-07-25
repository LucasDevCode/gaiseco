import spacy
from spacy_layout import spaCyLayout

import pdfplumber

def pdf_to_txt_spacy(pdf_path: str, txt_path: str):    
    nlp = spacy.blank("en")
    layout = spaCyLayout(nlp)

    doc = layout(pdf_path)

    txt_path = txt_path[ : txt_path.rfind('.') ]
    with open(file=txt_path+'_spacy.txt', mode='w', encoding='utf-8') as f:
        f.write(doc.text)


def pdf_to_txt_pdfplumber(pdf_path: str, txt_path: str):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    txt_path = txt_path[ : txt_path.rfind('.') ]
    with open(file=txt_path+'_pdfplumber.txt', mode='w', encoding='utf-8') as f:
        f.write(text)



from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(uploaded_file):
    filename = uploaded_file.name.lower()
    uploaded_file.seek(0)

    if filename.endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(
            paragraph.text for paragraph in doc.paragraphs
        )

    elif filename.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    else:
        raise ValueError("Please upload a PDF or DOCX file.")
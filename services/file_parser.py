# services/file_parser.py
from io import BytesIO
import PyPDF2
from docx import Document

def get_file_text(uploaded_file):
    """Extracts text from PDF, DOCX, or TXT file."""
    text = ""
    file_name = uploaded_file.name
    if file_name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.read()))
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif file_name.endswith('.docx'):
        doc = Document(BytesIO(uploaded_file.read()))
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_name.endswith('.txt'):
        text = uploaded_file.read().decode('utf-8')
    return text
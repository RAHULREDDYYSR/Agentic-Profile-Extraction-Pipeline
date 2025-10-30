from io import BytesIO
from docx import Document
import fitz  # PyMuPDF library

def get_file_text(uploaded_file):
    """
    Extracts text and embedded hyperlinks from PDF, DOCX, or TXT files.
    For PDFs, it appends all found URLs to the end of the text to give the LLM full context.
    """
    text = ""
    file_name = uploaded_file.name
    
    if file_name.endswith('.pdf'):
        try:
            # Read the file into memory
            pdf_bytes = BytesIO(uploaded_file.read())
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            all_links = []
            # Iterate through each page to extract text and links
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text")  # Extract plain text
                
                # Extract all hyperlink URIs from the page
                links = page.get_links()
                for link in links:
                    if link.get('uri'):
                        all_links.append(link['uri'])
            
            # De-duplicate links and append them to the text
            if all_links:
                unique_links = sorted(list(set(all_links)))
                text += "\n\n--- DETECTED HYPERLINKS ---\n"
                for link in unique_links:
                    text += f"- {link}\n"
                    
        except Exception as e:
            print(f"Error parsing PDF with PyMuPDF: {e}")
            return "" # Return empty string on failure

    elif file_name.endswith('.docx'):
        doc = Document(BytesIO(uploaded_file.read()))
        for para in doc.paragraphs:
            text += para.text + "\n"
            
    elif file_name.endswith('.txt'):
        text = uploaded_file.read().decode('utf-8')
        
    return text
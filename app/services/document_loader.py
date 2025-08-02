# app/services/document_loader.py

import fitz  # PyMuPDF

def load_document(file_path: str) -> str:
    """Extracts text from PDF"""
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        raise RuntimeError(f"Failed to load document: {str(e)}")
    return text.strip()

import os
from pypdf import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Safely extracts text from a PDF file.
    Returns: String (Text content) or None (if error).
    """
    if not os.path.exists(pdf_path):
        print(f"[Error] File not found: {pdf_path}")
        return None
    
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        
        # Basic cleaning
        if len(text.strip()) < 50:
            print("[Warning] PDF text is too short or empty. Is it an image scan?")
            return None
            
        return text.strip()
        
    except Exception as e:
        print(f"[Error] Failed to read PDF: {e}")
        return None
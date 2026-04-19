from io import BytesIO
from PyPDF2 import PdfReader


def extract_text(filename: str, content: bytes) -> str:
    lower = filename.lower()
    if lower.endswith('.txt'):
        return content.decode('utf-8', errors='ignore').strip()

    if lower.endswith('.pdf'):
        reader = PdfReader(BytesIO(content))
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or '')
        return '\n'.join(pages).strip()

    raise ValueError('Unsupported file type. Please upload a PDF or TXT file.')

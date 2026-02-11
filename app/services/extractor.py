"""
Extraction texte depuis PDF avec pdfplumber.
Pas d'OCR, juste le texte natif du PDF.
"""

import base64
import tempfile
import pdfplumber


def extract_text_from_base64(pdf_base64: str) -> str:
    """Décode un PDF base64 et extrait le texte de chaque page."""
    clean_b64 = pdf_base64.replace("data:application/pdf;base64,", "")
    pdf_bytes = base64.b64decode(clean_b64)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        return _extract(tmp.name)


def extract_text_from_bytes(pdf_bytes: bytes) -> str:
    """Extrait le texte depuis des bytes bruts (upload multipart)."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
        tmp.write(pdf_bytes)
        tmp.flush()
        return _extract(tmp.name)


def _extract(path: str) -> str:
    """Lit chaque page du PDF et concatène le texte."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                pages.append(text.strip())

            # Extraire les tableaux aussi
            for table in page.extract_tables():
                if table:
                    rows = [" | ".join(str(c or "") for c in row) for row in table]
                    pages.append("[Tableau]\n" + "\n".join(rows))

    return "\n\n".join(pages)

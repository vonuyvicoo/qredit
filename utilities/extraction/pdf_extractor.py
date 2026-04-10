import io

import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes

from utilities.extraction.base_extractor import BaseExtractor


class PDFExtractor(BaseExtractor):
    async def extract(self, content: bytes) -> str:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            ).strip()

        if text:
            return text

        images = convert_from_bytes(content)
        return "\n".join(pytesseract.image_to_string(img) for img in images)

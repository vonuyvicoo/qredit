import io

import pytesseract
from docx import Document
from docx.oxml.ns import qn
from PIL import Image

from utilities.extraction.base_extractor import BaseExtractor


class DOCXExtractor(BaseExtractor):
    async def extract(self, content: bytes) -> str:
        doc = Document(io.BytesIO(content))

        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

        image_texts: list[str] = []
        for rel in doc.part.rels.values():
            if "image" in rel.reltype:
                image_data = rel.target_part.blob
                image = Image.open(io.BytesIO(image_data))
                image_texts.append(pytesseract.image_to_string(image))

        return "\n".join(paragraphs + image_texts)

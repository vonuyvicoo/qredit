import io

import pytesseract
from PIL import Image

from utilities.extraction.base_extractor import BaseExtractor


class ImageExtractor(BaseExtractor):
    async def extract(self, content: bytes) -> str:
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

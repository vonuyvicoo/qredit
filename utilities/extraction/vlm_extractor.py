import io

import pytesseract
from PIL import Image

from utilities.extraction.base_extractor import BaseExtractor

#vision language models
#the core idea behind this is just to extract text. NOT structured output. 
# we will pipe text from here to a transformer utility for actual structured output
class VLMExtractor(BaseExtractor):
    async def extract(self, content: bytes) -> str:
        image = Image.open(io.BytesIO(content))
        return pytesseract.image_to_string(image)

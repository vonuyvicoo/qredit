from utilities.extraction.base_extractor import BaseExtractor

class RawTextExtractor(BaseExtractor):
    async def extract(self, content: bytes) -> str:
        return content.decode("utf-8", errors="ignore")

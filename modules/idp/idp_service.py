from modules.document.document_service import document_service 
from utilities.extraction.extractor_factory import ExtractorFactory 

class IDPService:
    def __init__(self) -> None:
        self.document_service = document_service 

    async def extract(self, file_id: str, client_id: str):
        file = await self.document_service.get_content(file_id, client_id)
        extractor = ExtractorFactory.create(file)
        text = extractor.extract(file)

        return text

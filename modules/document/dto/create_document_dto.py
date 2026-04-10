from pydantic import BaseModel

from modules.document.types.enums import DocumentTypeEnum


class CreateDocumentDto(BaseModel):
    filename: str
    document_type: DocumentTypeEnum
    password: str | None = None

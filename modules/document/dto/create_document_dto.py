from pydantic import BaseModel

from modules.document.types.enums import DocumentStatusEnum, DocumentTypeEnum


class CreateDocumentDto(BaseModel):
    filename: str
    document_type: DocumentTypeEnum 
    status: DocumentStatusEnum
    file_ref: str
    password: str | None = None


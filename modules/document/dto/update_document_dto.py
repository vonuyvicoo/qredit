from pydantic import BaseModel

from modules.document.types.enums import DocumentStatusEnum, DocumentTypeEnum

class UpdateDocumentDto(BaseModel):
    filename: str | None = None
    document_type: DocumentTypeEnum | None = None
    status: DocumentStatusEnum | None = None
    file_ref: str | None = None
    password: str | None = None

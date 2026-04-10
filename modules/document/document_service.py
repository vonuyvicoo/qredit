from fastapi import HTTPException, UploadFile
from prisma.models import Document
from prisma.types import DocumentCreateInput, DocumentUpdateInput

from database.config import db
from modules.document.dto.create_document_dto import CreateDocumentDto
from modules.document.dto.update_document_dto import UpdateDocumentDto
from modules.files.file_service import file_service


class DocumentService:
    def __init__(self) -> None:
        self.db = db

    async def find_many(self, client_id: str) -> list[Document]:
        return await self.db.document.find_many(
            where={"client_id": client_id}
        )

    async def find_one(self, id: str, client_id: str) -> Document:
        return await self.db.document.find_first_or_raise(
            where={"id": id, "client_id": client_id}
        )

    async def create(self, document: CreateDocumentDto, file: UploadFile, client_id: str) -> Document:
        uploaded = await file_service.create(client_id, file)

        return await self.db.document.create(
            data=DocumentCreateInput(
                **document.model_dump(),
                client_id=client_id,
                file_ref=uploaded["path"],
            )
        )

    async def update(self, id: str, document: UpdateDocumentDto, client_id: str) -> Document:
        await self.find_one(id, client_id)

        result = await self.db.document.update(
            where={"id": id},
            data=DocumentUpdateInput(**document.model_dump(exclude_none=True))
        )
        if result is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return result

    async def get_content(self, id: str, client_id: str) -> bytes:
        doc = await self.find_one(id, client_id)
        filename = doc.file_ref.split("/", 1)[-1]
        return file_service.get_content(client_id, filename)

    async def update_content(self, id: str, file: UploadFile, client_id: str) -> Document:
        doc = await self.find_one(id, client_id)
        filename = doc.file_ref.split("/", 1)[-1]
        await file_service.update(client_id, filename, file)
        return doc

    async def delete(self, id: str, client_id: str) -> None:
        doc = await self.find_one(id, client_id)
        filename = doc.file_ref.split("/", 1)[-1]
        file_service.delete(client_id, filename)

        try:
            await self.db.document.delete(where={"id": id})
        except Exception:
            raise HTTPException(status_code=404, detail="Document not found or already deleted.")


document_service = DocumentService()

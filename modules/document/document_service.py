from fastapi import HTTPException
from prisma.models import Document
from prisma.types import DocumentCreateInput, DocumentUpdateInput

from database.config import db
from modules.document.dto.create_document_dto import CreateDocumentDto
from modules.document.dto.update_document_dto import UpdateDocumentDto


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

    async def create(self, document: CreateDocumentDto, client_id: str) -> Document:
        return await self.db.document.create(
            data=DocumentCreateInput(
                **document.model_dump(),
                client_id=client_id,
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

    async def delete(self, id: str, client_id: str) -> None:
        await self.find_one(id, client_id)

        try:
            await self.db.document.delete(
                where={"id": id}
            )
        except Exception:
            raise HTTPException(status_code=404, detail="Document not found or already deleted.")


document_service = DocumentService()

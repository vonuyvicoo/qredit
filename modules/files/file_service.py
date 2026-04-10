from fastapi import HTTPException, UploadFile

from config import config
from database.supabase import supabase


class FileService:
    def __init__(self) -> None:
        self.storage = supabase.storage.from_(config.SUPABASE_BUCKET)

    def _path(self, client_id: str, filename: str) -> str:
        return f"{client_id}/{filename}"

    def find_many(self, client_id: str) -> list:
        return self.storage.list(client_id)

    def find_one(self, client_id: str, filename: str) -> dict:
        files = self.storage.list(client_id)
        match = next((f for f in files if f["name"] == filename), None)
        if match is None:
            raise HTTPException(status_code=404, detail="File not found")
        return match

    def get_content(self, client_id: str, filename: str) -> bytes:
        try:
            return self.storage.download(self._path(client_id, filename))
        except Exception:
            raise HTTPException(status_code=404, detail="File not found")

    async def create(self, client_id: str, file: UploadFile) -> dict:
        contents = await file.read()
        path = self._path(client_id, file.filename or "unnamed")

        try:
            response = self.storage.upload(
                path=path,
                file=contents,
                file_options={"content-type": file.content_type or "application/octet-stream", "upsert": "false"},
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {"path": path, "id": response.path}

    async def update(self, client_id: str, filename: str, file: UploadFile) -> dict:
        contents = await file.read()
        path = self._path(client_id, filename)

        try:
            response = self.storage.update(
                path=path,
                file=contents,
                file_options={"content-type": file.content_type or "application/octet-stream", "upsert": "true"},
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {"path": path, "id": response.path}

    def delete(self, client_id: str, filename: str) -> None:
        try:
            self.storage.remove([self._path(client_id, filename)])
        except Exception:
            raise HTTPException(status_code=404, detail="File not found")


file_service = FileService()

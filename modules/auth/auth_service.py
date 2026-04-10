import secrets

from fastapi import HTTPException
from starlette import status

from database.config import db
from modules.auth.dto.login_dto import LoginDto
from modules.auth.dto.register_dto import RegisterDto
from utilities.encryption import EncryptionUtils
from utilities.jwtUtils import create_access_token


class AuthService:
    def __init__(self) -> None:
        self.db = db

    async def register(self, body: RegisterDto) -> dict:
        plain_token = secrets.token_urlsafe(32)
        encrypted = EncryptionUtils.encrypt(plain_token)

        client = await self.db.client.create(data={
            "name": body.name,
            "encrypted_token": encrypted,
        })

        return {"client_id": client.id, "secret": plain_token}

    async def login(self, body: LoginDto) -> str:
        client = await self.db.client.find_unique(where={"id": body.client_id})

        if client is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        try:
            plain = EncryptionUtils.decrypt(client.encrypted_token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if plain != body.secret:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        return create_access_token(payload={"client_id": client.id})


auth_service = AuthService()

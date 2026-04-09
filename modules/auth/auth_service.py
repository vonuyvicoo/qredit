from datetime import timedelta

from fastapi import HTTPException
from prisma.models import User
from starlette import status

from database.config import db
from modules.auth.dto.login_dto import LoginDto
from modules.user.dto.create_user_dto import CreateUserDto
from utilities.bcrypt_hashing import HashingUtils
from utilities.jwtUtils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


def register(body: CreateUserDto) -> User:
    existing = db.user.find_unique(where={"email": body.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email already exist"
        )

    body.password = HashingUtils.hash(body.password)

    return db.user.create(data={
        "name": body.name,
        "email": body.email,
        "password": body.password,
    })


def login(body: LoginDto) -> str:
    user = db.user.find_unique(where={"email": body.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email not found"
        )

    if not HashingUtils.validate(plain_password=body.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid Password"
        )

    return create_access_token(
        payload={"user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

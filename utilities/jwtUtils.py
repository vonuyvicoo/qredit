from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from config import config

ACCESS_TOKEN_EXPIRE_MINUTES = 30
http_bearer = HTTPBearer(scheme_name="JWT")


class JwtPayload(BaseModel):
    client_id: str

def create_access_token(payload: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = payload.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60 * 24 * 14)  # 14d

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, config.HASH_SALT, algorithm=config.HASH_ALGORITHM)


def validate_token(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)], payload_return: bool = False):
    try:
        payload = jwt.decode(token.credentials, config.HASH_SALT, algorithms=[config.HASH_ALGORITHM])
        client_id = payload.get("client_id")

        if client_id is None:
            raise InvalidTokenError

        if payload_return:
            return payload

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalid or Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_payload(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]) -> JwtPayload:
    try:
        payload = jwt.decode(token.credentials, config.HASH_SALT, algorithms=[config.HASH_ALGORITHM])
        client_id = payload.get("client_id")
        if client_id is None:
            raise InvalidTokenError
        return JwtPayload(**payload)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalid or Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def refreshJwtToken(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]):
    payload = validate_token(payload_return=True, token=token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid auth payload"
        )

    newToken = create_access_token(payload=payload)
    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail={
            "status": "True",
            "message": "Success Refresh Token",
            "token": newToken
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

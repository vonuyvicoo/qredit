from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Any

import jwt, os
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

load_dotenv(".env")

SECRET_KEY = os.getenv("HASH_SALT")
ALGORITHM = os.getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = HTTPBearer(scheme_name="JWT")

class TokenData(BaseModel):
    username: Union[str, None] = None

def create_access_token(payload: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = payload.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(payload_return: bool = False, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)] = None):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise InvalidTokenError
        if payload_return:
            return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalid or Expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

def refreshJwtToken(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]):
    payload = validate_token(payload_return=True, token=token)
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

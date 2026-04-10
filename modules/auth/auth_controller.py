from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from modules.auth.auth_service import auth_service
from modules.auth.dto.login_dto import LoginDto
from modules.auth.dto.register_dto import RegisterDto
from utilities.jwtUtils import validate_token, refreshJwtToken

router = APIRouter(prefix="/auth", tags=["Auth"], default_response_class=JSONResponse)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(body: RegisterDto):
    return await auth_service.register(body)


@router.post("/login")
async def login(body: LoginDto):
    token = await auth_service.login(body)
    return {"token": token, "type": "bearer"}


@router.post("/validate-token", dependencies=[Depends(validate_token)])
async def validate_token_route():
    return {"message": "Token valid"}


@router.post("/refresh-token", dependencies=[Depends(refreshJwtToken)])
async def refresh_token_route():
    pass

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from modules.auth import auth_service
from modules.auth.dto.login_dto import LoginDto
from modules.user.dto.create_user_dto import CreateUserDto
from utilities.jwtUtils import validate_token, refreshJwtToken

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_route(body: CreateUserDto) -> JSONResponse:
    user = auth_service.register(body)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "status": "success",
            "message": "User created successfully",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": str(user.created_at),
                "updated_at": str(user.updated_at),
            }
        }
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_route(body: LoginDto) -> JSONResponse:
    token = auth_service.login(body)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Login successfully",
            "token": token,
            "type": "bearer"
        }
    )


@router.post("/validate-token", status_code=status.HTTP_200_OK, dependencies=[Depends(validate_token)])
async def validate_token_route():
    return {"message": "Token valid"}


@router.post("/refresh-token", status_code=status.HTTP_200_OK, dependencies=[Depends(refreshJwtToken)])
async def refresh_token_route():
    pass

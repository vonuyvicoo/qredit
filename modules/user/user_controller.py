from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from modules.user import user_service
from utilities.jwtUtils import validate_token, refreshJwtToken

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(validate_token)])
async def get_users_route() -> JSONResponse:
    users = user_service.get_users()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "message": "Success get all users",
            "data": jsonable_encoder(users),
        }
    )

from fastapi import APIRouter

from modules.auth.auth_controller import router as auth_router
from modules.user.user_controller import router as user_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(user_router)


@router.get("/", tags=["Health"])
async def root():
    return {"message": "Hello World"}

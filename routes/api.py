from fastapi import APIRouter

from modules.auth.auth_controller import router as auth_router
from modules.document.document_controller import router as document_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(document_router)

@router.get("/", tags=["Health"])
async def root():
    return {"message": "Hello World"}

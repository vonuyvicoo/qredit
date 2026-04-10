from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

from modules.document.document_service import document_service
from modules.document.dto.create_document_dto import CreateDocumentDto
from modules.document.dto.update_document_dto import UpdateDocumentDto 

from utilities.guards import AuthGuard
from utilities.jwtUtils import JwtPayload, get_payload

router = APIRouter(prefix="/documents", tags=["Documents"], default_response_class=JSONResponse, dependencies=[AuthGuard])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    document: CreateDocumentDto, 
    jwt_payload: Annotated[JwtPayload, Depends(get_payload)]
):
    doc = await document_service.create(document, jwt_payload.client_id)
    return jsonable_encoder(doc)

@router.get("/")
async def find_many(jwt_payload: Annotated[JwtPayload, Depends(get_payload)]):
    client_id: str = jwt_payload.client_id;

    docs = await document_service.find_many(client_id)
    return docs

@router.get("/{id}")
async def fine_one(
    id: str,
    jwt_payload: Annotated[JwtPayload, Depends(get_payload)]
):
    doc = await document_service.find_one(id, jwt_payload.client_id)
    return doc

@router.patch("/{id}")
async def patch(
    id: str, 
    document: UpdateDocumentDto,
    jwt_payload: Annotated[JwtPayload, Depends(get_payload)]
):
    doc = await document_service.update(id, document, jwt_payload.client_id)
    return doc

@router.delete("/{id}")
async def delete(
    id: str,
    jwt_payload: Annotated[JwtPayload, Depends(get_payload)] 
):
    doc = await document_service.delete(id, jwt_payload.client_id)
    return doc

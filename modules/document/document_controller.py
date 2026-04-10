from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from starlette import status as http_status
from starlette.responses import JSONResponse

from modules.document.document_service import document_service
from modules.document.dto.create_document_dto import CreateDocumentDto
from modules.document.types.enums import DocumentTypeEnum
from modules.document.dto.update_document_dto import UpdateDocumentDto
from utilities.guards import AuthGuard
from utilities.jwtUtils import JwtPayload, get_payload

router = APIRouter(prefix="/documents", tags=["Documents"], default_response_class=JSONResponse, dependencies=[AuthGuard])


@router.get("/")
async def find_many(payload: Annotated[JwtPayload, Depends(get_payload)]):
    docs = await document_service.find_many(payload.client_id)
    return jsonable_encoder(docs)


@router.get("/{id}")
async def find_one(id: str, payload: Annotated[JwtPayload, Depends(get_payload)]):
    doc = await document_service.find_one(id, payload.client_id)
    return jsonable_encoder(doc)


@router.get("/{id}/content")
async def get_content(id: str, payload: Annotated[JwtPayload, Depends(get_payload)]):
    content = await document_service.get_content(id, payload.client_id)
    return Response(content=content, media_type="application/octet-stream")


@router.post("/", status_code=http_status.HTTP_201_CREATED)
async def create(
    payload: Annotated[JwtPayload, Depends(get_payload)],
    filename: str = Form(...),
    document_type: DocumentTypeEnum = Form(...),
    password: str | None = Form(None),
    file: UploadFile = File(...),
):
    document = CreateDocumentDto(filename=filename, document_type=document_type, password=password)
    doc = await document_service.create(document, file, payload.client_id)
    return jsonable_encoder(doc)


@router.patch("/{id}")
async def update(id: str, document: UpdateDocumentDto, payload: Annotated[JwtPayload, Depends(get_payload)]):
    doc = await document_service.update(id, document, payload.client_id)
    return jsonable_encoder(doc)


@router.patch("/{id}/content")
async def update_content(
    id: str,
    payload: Annotated[JwtPayload, Depends(get_payload)],
    file: UploadFile = File(...),
):
    doc = await document_service.update_content(id, file, payload.client_id)
    return jsonable_encoder(doc)


@router.delete("/{id}", status_code=http_status.HTTP_204_NO_CONTENT)
async def delete(id: str, payload: Annotated[JwtPayload, Depends(get_payload)]):
    await document_service.delete(id, payload.client_id)

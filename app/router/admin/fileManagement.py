import json
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request, Body

from model.fileModel import ChangeStatusRequest, UpdateFileRequest
from services.fileService import FileService

router = APIRouter(prefix="/admin", tags=["admin","file"])
service = FileService()

@router.get("/get_all_files")
async def get_all_files(request: Request):
    return await service.get_all_files(request)

@router.put("/upload")
async def upload(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(...),
    name: str = Form(...)
):
    tags = json.loads(tags)
    return await service.upload_file(request=request, file=file, tags=tags,name=name)

@router.post("/change_status")
async def change_status(request: Request, body: ChangeStatusRequest):
    return await service.change_status(request, body)

@router.post("/update_file")
async def update_file(
    request: Request,
    file: UploadFile = File(None),
    tags: str = Form(...),
    file_id: int = Form(...),
    name: str = Form(...)
):
    tags = json.loads(tags)
    return await service.update_file(request, file, tags, file_id, name)

@router.post("/change tags")
async def change_tags(
    request: Request,
    tags: List[int] = Body(...),
    file_id: int = Body(...)
):
    pass

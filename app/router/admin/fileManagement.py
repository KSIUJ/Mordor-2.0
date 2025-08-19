import json

from fastapi import APIRouter, UploadFile, File, Form, Request

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
    tags: str = Form(...)
):
    tags = json.loads(tags)
    return await service.upload_file(request=request, file=file, tags=tags)

@router.post("/change_status")
async def change_status(request: Request, body: ChangeStatusRequest):
    return await service.change_status(request, body)

@router.post("/update_file")
async def update_file(
    request: Request,
    file: UploadFile = File(...),
    body: str = Form(...)
):
    data = json.loads(body)
    update_request = UpdateFileRequest(**data)
    return await service.update_file(request, file, update_request,1)

import json
from typing import List

from fastapi import APIRouter, UploadFile, File, Form,Request, Body
from starlette.responses import RedirectResponse

from model.fileModel import ChangeStatusRequest, ChangeTagsRequest, FileStatus
from services.fileService import FileService
from utils.errorWrapper import handle_file_service_errors

router = APIRouter(prefix="/admin", tags=["admin","file"])
service = FileService()



@router.get("/all_files")
@handle_file_service_errors
async def get_all_files():
    return await service.get_all_files()

@router.post("/file")
@handle_file_service_errors
async def upload(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(...),
    name: str = Form(...)
):
    userId = 1
    # TODO: Enable getting id of logged user
    if tags is None:
        tags = []
    else:
        tags = json.loads(tags)
    await service.upload_file(request=request, file=file, tags=tags, name=name, userId=userId)
    return RedirectResponse(url="/upload",status_code=303)
@router.post("/change_status")
@handle_file_service_errors
async def change_status(
    file_id: int = Form(...),
    status: FileStatus = Form(...),
    version: int = Form(...)
):
    req=ChangeStatusRequest(file_id=file_id, status=status,version=version)
    await service.change_status(req)
    return RedirectResponse(url="/update",status_code=303)

@router.post("/file/{file_id}")
@handle_file_service_errors
async def update_file(
    file_id: int,
    file: UploadFile = File(...),
    tags: str = Form(None),
    name: str = Form(...),

):
    if tags is None:
        tags=[]
    else:
        tags = json.loads(tags)
    await service.update_file(file=file, tags=tags, fileId=file_id, name=name)
    return RedirectResponse(url="/update",status_code=303)

@router.post("/change_tags")
@handle_file_service_errors
async def change_tags(
    changeReq: ChangeTagsRequest = Body(...)
):
    return await service.change_tags(changeReq.file_id,changeReq.tags)

@router.delete("/file/{file_id}")
@handle_file_service_errors
async def delete_file(
    file_id: int
):
    return await service.delete_file(file_id)

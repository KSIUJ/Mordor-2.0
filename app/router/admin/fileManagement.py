import json
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request, Body
from starlette.responses import RedirectResponse

from model.fileModel import ChangeStatusRequest, ChangeTagsRequest
from services.fileService import FileService
from utils.errorWrapper import handle_file_service_errors

router = APIRouter(prefix="/admin", tags=["admin","file"])
service = FileService()



@router.get("/get_all_files")
@handle_file_service_errors
async def get_all_files(request: Request):
    return await service.get_all_files(request)

@router.post("/upload")
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
    return RedirectResponse(url="/update",status_code=303)
@router.post("/change_status")
@handle_file_service_errors
async def change_status(request: Request, body: ChangeStatusRequest):
    await service.change_status(request, body)
    # return RedirectResponse(url="/update",status_code=303)
    return None

@router.post("/update_file")
@handle_file_service_errors
async def update_file(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(None),
    file_id: int = Form(...),
    name: str = Form(...)
):
    if tags is None:
        tags=[]
    else:
        tags = json.loads(tags)
    await service.update_file(request,file, tags, file_id, name)
    return RedirectResponse(url="/update",status_code=303)

@router.post("/change_tags")
@handle_file_service_errors
async def change_tags(
    request: Request,
    changeReq: ChangeTagsRequest = Body(...)
):
    return await service.change_tags(request, changeReq.file_id,changeReq.tags)

@router.delete("/delete_file/{file_id}")
@handle_file_service_errors
async def delete_file(
    request: Request,
    file_id: int
):
    return await service.delete_file(request, file_id)

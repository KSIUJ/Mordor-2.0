import json
from typing import List

from fastapi import APIRouter, UploadFile, File, Form, Request, Body, HTTPException
from functools import wraps
from model.fileModel import ChangeStatusRequest, UpdateFileRequest, ChangeTagsRequest
from services.fileService import FileService

router = APIRouter(prefix="/admin", tags=["admin","file"])
service = FileService()

#   =============== ERROR HANDLING WRAPPER ==================
def handle_service_errors(func):
    """Decorator for handling errors"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except PermissionError as e:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to perform this action"
            )
        except FileNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=409,
                detail="Users cannot modify accepted files"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
    wrapper.__name__ = func.__name__
    wrapper.__annotations__ = func.__annotations__
    wrapper.__doc__ = func.__doc__

    return wrapper

@router.get("/get_all_files")
@handle_service_errors
async def get_all_files(request: Request):
    return await service.get_all_files(request)

@router.put("/upload")
@handle_service_errors
async def upload(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(...),
    name: str = Form(...)
):
    userId = 1
    # TODO: Enable getting id of logged user
    tags = json.loads(tags)
    return await service.upload_file(request=request, file=file, tags=tags, name=name, userId=userId)

@router.post("/change_status")
@handle_service_errors
async def change_status(request: Request, body: ChangeStatusRequest):
    return await service.change_status(request, body)

@router.post("/update_file")
@handle_service_errors
async def update_file(
    request: Request,
    file: UploadFile = File(None),
    tags: str = Form(...),
    file_id: int = Form(...),
    name: str = Form(...)
):
    tags = json.loads(tags)
    return await service.update_file(request, file, tags, file_id, name)

@router.post("/change_tags")
@handle_service_errors
async def change_tags(
    request: Request,
    changeReq: ChangeTagsRequest = Body(...)
):
    return await service.change_tags(request, changeReq.file_id,changeReq.tags)

@router.delete("/delete_file/{file_id}")
@handle_service_errors
async def delete_file(
    request: Request,
    file_id: int
):
    return await service.delete_file(request, file_id)

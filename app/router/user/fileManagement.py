import json

from fastapi import APIRouter, UploadFile, File, Form, Request
from starlette.responses import RedirectResponse

from services.fileService import FileService
from utils.errorWrapper import handle_file_service_errors

router = APIRouter(prefix="/user", tags=["user", "file"])
service = FileService()

@router.post("/upload")
@handle_file_service_errors
async def upload(
        request: Request,
        file: UploadFile = File(...),
        tags: str = Form(...),
        name: str = Form(...)
):
    # user = await auth_service.get_user_from_cookie()
    userId = 1
    #TODO: Enable getting id of logged user
    tags = json.loads(tags)
    await service.upload_file(request=request, file=file, tags=tags, name=name, userId=userId)
    return RedirectResponse(url="/upload?success=file send successfully", status_code=303)

@router.post("/update_file")
@handle_file_service_errors
async def update_file(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(None),
    file_id: int = Form(...),
    name: str = Form(...)
):
    tags = json.loads(tags)
    return await service.update_file(request,file, tags,file_id, name)
    return RedirectResponse(url="/update",status_code=303)

@router.get("/get_files")
@handle_file_service_errors
async def get_files(request: Request):
    result = await service.get_accepted_files(request)
    return result
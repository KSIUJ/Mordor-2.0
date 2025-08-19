from fastapi import APIRouter, UploadFile, File, Form, Request

from services.authservice import auth_service
from services.fileService import FileService

router = APIRouter(prefix="/user", tags=["user", "file"])
service = FileService()


@router.put("/upload")
async def upload(
        request: Request,
        file: UploadFile = File(...),
        tags: list[int] = Form(...)

):
    # user = await auth_service.get_user_from_cookie()
    userId = 1
    #TODO: Enable getting id of logged user

    result = await service.upload_file(file=file, tags=tags, userId=userId, request=request)
    return result


@router.get("/get_files")
async def get_files(request: Request):
    result = await service.get_accepted_files(request)
    return result


from fastapi import APIRouter, UploadFile, File, Form

from model.fileModel import ChangeStatusRequest
from services.authservice import auth_service
from services.fileService import FileService
router = APIRouter(prefix="/admin", tags=["admin","file"])
service = FileService()
@router.put("/upload")
async def upload(
    file: UploadFile = File(...),
    tags: list[int]=Form(...)
):
    # user = await auth_service.get_user_from_cookie()
    userId=1
    #TODO: Enable getting id of logged user

    result= await service.upload_file(file=file,tags=tags,userId=userId)
    return result

@router.post("/change_status")
async def change_status(
        request: ChangeStatusRequest
):
    return await service.change_status(request)
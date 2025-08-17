
from fastapi import APIRouter, UploadFile, File, Form

from services.authservice import auth_service
from services.fileService import FileService
router = APIRouter(prefix="/admin", tags=["admin","file"])
@router.put("/upload")
async def upload(
    file: UploadFile = File(...),
    tags: list[int]=Form(...)
):
    # user = await auth_service.get_user_from_cookie()
    userId=1
    #TODO: Enable getting id of logged user
    service = FileService()
    result= await service.upload_file(file=file,tags=tags,userId=userId)
    return result
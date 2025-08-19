import json

from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException

from services.authservice import auth_service
from services.fileService import FileService

router = APIRouter(prefix="/user", tags=["user", "file"])
service = FileService()


@router.put("/upload")
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
    return await service.upload_file(request=request, file=file, tags=tags, name=name, userId=userId)




@router.post("/update_file")
async def update_file(
    request: Request,
    file: UploadFile = File(...),
    tags: str = Form(...),
    id: int = Form(...),
    name: str = Form(...)
):
    tags = json.loads(tags)
    return await service.update_file(request, file, tags,id, name)

@router.get("/get_files")
async def get_files(request: Request):
    result = await service.get_accepted_files(request)
    return result
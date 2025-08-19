import json

from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException

from services.authservice import auth_service
from services.fileService import FileService

router = APIRouter(prefix="/user", tags=["user", "file"])
service = FileService()

#   =============== ERROR HANDLING WRAPPER ==================
def handle_service_errors(func):
    """Decorator for handling errors"""
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
    return wrapper

@router.put("/upload")
@handle_service_errors
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
@handle_service_errors
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
@handle_service_errors
async def get_files(request: Request):
    result = await service.get_accepted_files(request)
    return result
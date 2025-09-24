import json

from fastapi import APIRouter, UploadFile, File, Form, Request, Query, HTTPException
from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse

from services.fileService import FileService
from utils.errorWrapper import handle_file_service_errors
from model.fileModel import FileStatus
from parser.parser import parseExpression

from typing import List

router = APIRouter(prefix="/user", tags=["user", "file"])
service = FileService()

@router.post("/file")
@handle_file_service_errors
async def upload(
        request: Request,
        file: UploadFile = File(...),
        tags: str = Form(None),
        name: str = Form(...)
):
    # user = await auth_service.get_user_from_cookie()
    userId = 1
    #TODO: Enable getting id of logged user
    tags = json.loads(tags)
    await service.upload_file(request=request, file=file, tags=tags, name=name, userId=userId)
    return RedirectResponse(url="/upload", status_code=303)

@router.post("/file/{file_id}")
@handle_file_service_errors
async def update_file(
    file_id: int,
    file: UploadFile = File(None),
    tags: str = Form(None),
    name: str = Form(...),

):
    tags = json.loads(tags)
    await service.update_file(file, tags,file_id, name)
    return RedirectResponse(url="/update",status_code=303)

@router.get("/files")
@handle_file_service_errors
async def get_files(request: Request):
    result = await service.get_accepted_files(request)
    return result

@router.get("/placeholder_search")
async def placeholder():
    return FileResponse("static/placeholder_search.html")

@router.get("/files")
@handle_file_service_errors
async def get_accepted_files_by_tags(q: str = Query("", max_length=250),
                                     status: List[FileStatus] = Query([FileStatus.ACCEPTED])):
    """
    Endpoint for searching files by tag expressions
    
    Args:
        q : Query string with logical tag expression
        status : list of selected file statuses

    Raises:
        400 BAD_REQUEST: Syntax errors in query expression

    Returns:
        List of files matching tag expression and status
    """
    try:
        
        q = q.strip()
        ast = parseExpression(q)
        results = await service.get_files_by_tags(ast, status)
        
        return results
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid syntax: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

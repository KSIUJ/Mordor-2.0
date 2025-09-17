import json

from fastapi import APIRouter, UploadFile, File, Form,Request, Query, HTTPException, Body, Response
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse

from services.fileService import FileService
from utils.errorWrapper import handle_file_service_errors
from model.fileModel import FileStatus
from parser.parser import parseExpression
from repository.fileRepository import file_repo

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


@router.get("/file/{file_id}")
async def get_file(file_id: int, request: Request):
     # Get file from database
    file = await file_repo.get_file_by_id(file_id)
    # Check if file exists and user has permission to download
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # For security, you might want to add additional checks here
    # For example: if file.status == FileStatus.ACCEPTED or user is admin
    
    # Return the file for download
    return FileResponse(
        path=file.filepath,
        filename=f"{file.name}.{file.filepath.split('.')[1]}",
        media_type='application/octet-stream'
    )

@router.get("/files")
@handle_file_service_errors
async def get_files():
    result = await service.get_accepted_files()
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
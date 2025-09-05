from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from services.authservice import Role
from fastapi.templating import Jinja2Templates
from repository.user_repository import user_repo
from repository.fileRepository import file_repo
from model.user import UserWithLimits
from model.fileModel import FileInfo, FileStatus
from typing import List
import logging

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["user"])


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to be in a readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

@router.get("/profile")
async def profile(request: Request):
    """
    Profile route
    """
    user : UserWithLimits = await user_repo.get_user_with_limits(request.state.user.id)
    files : List[FileInfo] = await file_repo.get_user_uploaded_files(user)
    for i, value in enumerate(files):
        files[i].status = files[i].status.value
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "name": user.username,
        "email" : user.email,
        "size_limit" : user.size_limit,
        "number_limit" : user.number_limit,
        "files" : files,
        "format_file_size": format_file_size
        })
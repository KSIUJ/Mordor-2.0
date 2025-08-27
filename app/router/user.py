from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from services.authservice import Role
from fastapi.templating import Jinja2Templates
from repository.user_repository import user_repo
from repository.fileRepository import file_repo
from model.user import UserWithLimits
from model.fileModel import FileInfo
from typing import List
import logging

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="", tags=["user"])



@router.get("/profile")
async def profile(request: Request):
    """
    Profile route
    """
    user : UserWithLimits = await user_repo.get_user_with_limits(request.state.user.id)
    files : List[FileInfo] = await file_repo.get_user_uploaded_files(user)
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "name": user.username,
        "email" : user.email,
        "size_limit" : user.size_limit,
        "number_limit" : user.number_limit,
        "files" : files
        })
    # Files not done(placeHolders) because file_repository is implemented in another PR and not yet merged
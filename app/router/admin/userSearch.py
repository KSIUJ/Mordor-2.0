from typing import List
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from model.user import User
from repository.user_repository import user_repo
from services.userService import UserService

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/admin", tags=["admin","user"])
service = UserService()

# TODO errorWrapper?
@router.get("/users")
async def get_all_users(request: Request):
    users : List[User] = await service.get_all_files(request)
    return templates.TemplateResponse("userSearch.html", {
        "request": request,
        "users": users
    })
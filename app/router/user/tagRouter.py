import json

from fastapi import APIRouter,Request
from repository.tagRepository import TagRepository

router = APIRouter(prefix="/user", tags=["user","tags"])
repo = TagRepository()

@router.get("/get_tags")
async def get_tags(request: Request):
    """No need for service"""
    return await repo.get_tags()
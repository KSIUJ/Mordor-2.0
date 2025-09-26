from fastapi import APIRouter
from repository.tagRepository import TagRepository

router = APIRouter(prefix="/user", tags=["user","tags"])
repo = TagRepository()

@router.get("/tags")
async def tags():
    """No need for service"""
    return await repo.get_tags()
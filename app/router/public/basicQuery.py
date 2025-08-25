import json

from fastapi import APIRouter,Request
from repository.publicRepository import PublicRepository

router = APIRouter(prefix="/public", tags=["public"])
repo = PublicRepository()

@router.get("/tags")
async def get_tags(request: Request):
    """No need for service"""
    return await repo.get_tags()
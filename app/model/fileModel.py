from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List

class FileStatus(str,Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class FileInfo(BaseModel):
    """Response model to return file to user"""
    id: int
    name: str
    size: int
    uploaded_by: int
    filepath: str
    status: FileStatus
    uploaded_at: datetime=None
    version:int =None


class AddFileRequest(BaseModel):
    """To add a file we need its model & selected tags"""
    filename: str
    filepath: str
    size: int
    status: FileStatus
    uploaded_by: int
    uploaded_at: datetime
    tags: List[int]

class UpdateFileRequest(BaseModel):
    """
    Modify basic info about file
    Does not affect tags
    """
    id: int
    filename: str
    size: int
    version: int
    uploaded_at: datetime

class ChangeStatusRequest(BaseModel):
    """To update status we just need id"""
    file_id: int
    status: FileStatus
    version: int

class ChangeTagsRequest(BaseModel):
    """To update tags we need id and new list of tags"""
    file_id: int
    tags: List[int]
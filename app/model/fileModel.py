from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List

class FileStatus(str,Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

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
    filepath: str
    size: int

class ChangeStatusRequest(BaseModel):
    """To update status we just need id"""
    fileId: int
    status: FileStatus
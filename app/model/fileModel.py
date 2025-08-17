from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List

class FileStatus(str,Enum):
    PENDING = "pending"
    APPROVED = "accepted"
    REJECTED = "rejected"

class FileInfo(BaseModel):
    """Response model to return file to user"""
    id: int
    name: str
    size: int
    uploaded_by: int
    status: FileStatus

class AcceptedFilesResponse(BaseModel):
    return_code: int
    files: List[FileInfo]

class AfterUploadResponse(BaseModel):
    return_code: int
    file_id: int
    tags: List[int]


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
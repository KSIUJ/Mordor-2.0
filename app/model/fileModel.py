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

class CommonResponse(BaseModel):
    """Response model to return file to user"""
    return_code: int
    message: str = None

class AcceptedFilesResponse(CommonResponse):
    files: List[FileInfo]

class AfterUploadResponse(CommonResponse):
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
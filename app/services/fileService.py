import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import UploadFile, Request, HTTPException
from model.fileModel import AddFileRequest, FileStatus, ChangeStatusRequest, UpdateFileRequest
from repository.fileRepository import FileRepository
from services.authservice import User, Role

#TODO: set correct path in docker-compose
UPLOAD_DIR=Path(os.getenv("UPLOAD_DIR", "uploads"))


# ==================== AUTH FUNCTIONS ====================
def admin_auth(request: Request):
    """For functions that require admin access"""
    user = request.state.user
    if user.role not in [Role.ADMIN]:
        raise PermissionError


def user_auth(request: Request):
    """For functions that require user access"""
    user = request.state.user
    if user.role not in [Role.ADMIN, Role.USER, Role.MANAGER]:
        raise PermissionError


# ==================== FILE OPERATIONS ====================
async def _save_file_to_disk(file: UploadFile) -> tuple[str, int]:
    """Save uploaded file to disk and return (filepath, size)"""
    ext = os.path.splitext(file.filename)[1]
    hashed_name = secrets.token_hex(16) + ext
    file_path = UPLOAD_DIR / hashed_name

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return str(file_path), len(content)


def _delete_file_if_exists(filepath: str):
    """Safely delete file if it exists"""

    #TODO: LOOK FOR DELETION ALTERNATIVE
    path = Path(filepath)
    if path.exists() and path.is_file():
        path.unlink()

# ==================== FILE SERVICE CLASS ====================
class FileService:
    def __init__(self):
        self.repo = FileRepository()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # ==================== ADMIN OPERATIONS ====================
    async def get_all_files(self, request: Request):
        admin_auth(request)
        return await self.repo.get_all_files()

    async def change_status(self, req: Request, request: ChangeStatusRequest):
        admin_auth(req)
        return await self.repo.change_status(request)

    async def change_tags(self, req: Request,fileId:int, tags: List[int]):
        admin_auth(req)
        return await self.repo.update_tags(fileId, tags)

    async def delete_file(self, req: Request, fileId: int):
        admin_auth(req)
        return await self.repo.delete_file(fileId)

    # ==================== USER OPERATIONS ====================
    async def get_accepted_files(self, request: Request):
        user_auth(request)
        return await self.repo.get_accepted_files()

    async def upload_file(self, request: Request, file: UploadFile,
                          tags: list[int], userId: int, name: str):
        user_auth(request)
        # Save file and get metadata
        filepath, size = await _save_file_to_disk(file)

        # Prepare request
        add_file_request = AddFileRequest(
            filename=name,
            filepath=filepath,
            size=size,
            uploaded_by=userId,
            status=FileStatus.PENDING,
            uploaded_at=datetime.now(),
            tags=tags
        )

        # Admin adds already accepted files
        if request.state.user.role == Role.ADMIN:
            add_file_request.status = FileStatus.ACCEPTED

        return await self.repo.insert_file_with_tags(add_file_request)

    async def update_file(self, request: Request, file: UploadFile,
                          tags: list[int], fileId: int, name: str):
        user_auth(request)

        # Get existing file
        existing_file = await self.repo.get_file_by_id(fileId)

        # Authorization checks
        self._validate_file_modification(existing_file, request.state.user)

        # Handle file operations
        filepath, size = await self._handle_file_operations(file, existing_file)

        # Prepare update request
        update_request = UpdateFileRequest(
            id=fileId,
            filename=name,
            filepath=filepath,
            size=size,
        )

        return await self.repo.update_file(update_request, tags)

    # ==================== PRIVATE HELPER METHODS ====================
    def _validate_file_modification(self, file, user: User):
        """Validate if user can modify the file"""
        if file.status != FileStatus.PENDING and user.role == Role.USER:
            #   TODO maybe change type
            raise ValueError

        # TODO: Add ownership check
        # if file.uploaded_by != user.id and user.role == Role.USER:
        #     raise HTTPException(status_code=403, detail="Not your file")

    def _handle_file_operations(self, file: UploadFile, existing_file) -> tuple[str, int]:
        """Handle file operations for update and return (filepath, size)"""
        if file:
            # Delete old file and save new one
            _delete_file_if_exists(existing_file.filepath)
            return _save_file_to_disk(file)
        else:
            # Keep existing file
            return existing_file.filepath, existing_file.size
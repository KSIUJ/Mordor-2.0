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
        return await self.repo.get_all_files()

    async def change_status(self, req: Request, request: ChangeStatusRequest):
        return await self.repo.change_status(request)

    async def change_tags(self, req: Request,fileId:int, tags: List[int]):
        return await self.repo.update_tags(fileId, tags)

    async def delete_file(self, req: Request, fileId: int):
        return await self.repo.delete_file(fileId)

    # ==================== USER OPERATIONS ====================
    async def get_accepted_files(self, request: Request):
        return await self.repo.get_accepted_files()

    async def upload_file(self, request: Request, file: UploadFile,
                          tags: list[int], userId: int, name: str):
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

        existing_file = await self.repo.get_file_by_id(fileId)

        # if existing_file.status != FileStatus.PENDING:
        #     raise HTTPException(status_code=403, detail=f"File {fileId} is not pending.")
        if file:

            # Delete old file
            filePath = Path(existing_file.filepath)

            if filePath.exists():
                #change content
                with open(filePath, "wb") as f:
                    content = await file.read()
                    f.write(content)
                    size=len(content)
        updateFileRequest = UpdateFileRequest(
            id=fileId,
            filename=name,
            size=size,
            uploaded_at=datetime.now(),
            version=existing_file.version+1
        )
        return await self.repo.update_file(updateFileRequest, tags)

    # ==================== PRIVATE HELPER METHODS ====================
    def _validate_file_modification(self, file, user: User):
        """Validate if user can modify the file"""
        if file.status != FileStatus.PENDING:
            #   TODO maybe change type
            raise ValueError

        # TODO: Add ownership check
        # if file.uploaded_by != user.id and user.role == Role.USER:
        #     raise HTTPException(status_code=403, detail="Not your file")
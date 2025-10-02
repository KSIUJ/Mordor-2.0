import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import UploadFile, Request, HTTPException
from model.fileModel import AddFileRequest, FileStatus, ChangeStatusRequest, UpdateFileRequest
from repository.fileRepository import FileRepository
from repository.limitsRepository import LimitsRepository
from services.authservice import User, Role

#TODO: set correct path in docker-compose
UPLOAD_DIR=Path(os.getenv("UPLOAD_DIR", "uploads"))

def _delete_file_if_exists(filepath: str):
    """Safely delete file if it exists"""

    #TODO: LOOK FOR DELETION ALTERNATIVE
    path = Path(filepath)
    if path.exists() and path.is_file():
        os.remove(filepath)

# ==================== FILE SERVICE CLASS ====================
class FileService:
    def __init__(self):
        self.repo = FileRepository()
        self.limits = LimitsRepository()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # ==================== ADMIN OPERATIONS ====================
    async def get_all_files(self):
        return await self.repo.get_all_files()

    async def change_status(self, request: ChangeStatusRequest):
        existing_file= await self.repo.get_file_by_id(request.file_id)
        if existing_file.version != request.version:
            #TODO : modify code
            raise PermissionError
        return await self.repo.change_status(request)

    async def change_tags(self, fileId:int, tags: List[int]):
        return await self.repo.update_tags(fileId, tags)

    async def delete_file(self,  fileId: int):
        file = await self.repo.get_file_by_id(fileId)
        _delete_file_if_exists(file.filepath)
        return await self.repo.delete_file(fileId)

    # ==================== USER OPERATIONS ====================
    async def get_accepted_files(self):
        return await self.repo.get_accepted_files()
    
    async def get_files_by_tags(self, ast, status: List[FileStatus]):
        return await self.repo.get_files_by_tags(ast, status)

    async def upload_file(self, request: Request, file: UploadFile,
                          tags: list[int], userId: int, name: str):
        # Save file and get metadata
        if not await self.limits.countOverflow(userId, request.state.role):
            raise PermissionError
        filepath, size = await self._save_file_to_disk(file,userId)


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
        if request.state.role == Role.ADMIN:
            add_file_request.status = FileStatus.ACCEPTED

        return await self.repo.insert_file_with_tags(add_file_request)

    async def update_file(self, file: UploadFile,
                          tags: list[int], fileId: int, name: str):

        existing_file = await self.repo.get_file_by_id(fileId)
        # if existing_file.status != FileStatus.PENDING:
        #     raise HTTPException(status_code=403, detail=f"File {fileId} is not pending.")
        if file:

            # Change old file
            filePath = Path(existing_file.filepath)
            if filePath.exists():
                #change content
                with open(filePath, "wb") as f:
                    content = await file.read()
                    # TODO: UPDATE LIMITS & UNCOMMENT FOLLOWING LINES
                    # if not self.limits.sizeOverflow(existing_file.uploaded_by, len(content)-existing_file.size):
                    #     raise PermissionError
                    f.write(content)
                    size=len(content)

                # !!! DON'T FORGET TO CHANGE EXTENSION WHILE MODIFYING FILE !!!
                uploaded_ext = Path(file.filename).suffix
                existing_file.filepath = filePath.with_suffix(uploaded_ext)
                if filePath!= existing_file.filepath:
                        filePath.rename(existing_file.filepath)

        else: size=existing_file.size
        # return existing_file.filepath
        updateFileRequest = UpdateFileRequest(
            id=fileId,
            filename=name,
            filepath=str(existing_file.filepath),
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
        # if file.uploaded_by != user.id and request.state.role == Role.USER:
        #     raise HTTPException(status_code=403, detail="Not your file")

    # ==================== FILE OPERATIONS ====================
    async def _save_file_to_disk(self,file: UploadFile, userId: int) -> tuple[str, int]:
        """Save uploaded file to disk and return (filepath, size)"""
        ext = os.path.splitext(file.filename)[1]
        hashedName = secrets.token_hex(16) + ext
        filePath = UPLOAD_DIR / hashedName

        with open(filePath, "wb") as f:
            content = await file.read()
            # TODO: UPDATE LIMITS & UNCOMMENT FOLLOWING LINES
            # if not self.limits.sizeOverflow(userId,len(content)):
            #     raise PermissionError
            f.write(content)

        return str(filePath), len(content)
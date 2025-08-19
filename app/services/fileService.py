import os
import secrets
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile, Request, HTTPException
from model.fileModel import AddFileRequest, FileStatus, ChangeStatusRequest
from repository.fileRepository import FileRepository
from services.authservice import User, Role

#TODO: update path to make it correct
UPLOAD_DIR=Path("uploads")

def admin_auth(request: Request):
    """For functions that require admin access"""

    user = request.state.user
    if user.role not in [Role.ADMIN]:
        raise HTTPException(status_code=403, detail="Permission denied")


def user_auth(request: Request):
    """For functions that require user access"""
    user = request.state.user
    if user.role not in [Role.ADMIN,Role.USER,Role.MANAGER]:
        raise HTTPException(status_code=403, detail="Permission denied")


class FileService:
    def __init__(self):
        self.repo = FileRepository()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    #     FROM ADMIN ROUTER

    async def get_all_files(self,request: Request):
        admin_auth(request)
        return await self.repo.get_all_files()

    async def change_status(self,req: Request,request: ChangeStatusRequest):
        admin_auth(req)
        return await self.repo.change_status(request)

    #      FROM USER ROUTER

    async def upload_file(self,request: Request,file: UploadFile, tags: list[int],userId: int):
        user_auth(request)

        # generate hashed name
        ext=os.path.splitext(file.filename)[1]
        hashedName=secrets.token_hex(16)+ext
        filePath=UPLOAD_DIR / hashedName

        #save to disk
        with open(filePath, "wb") as f:
            content=await file.read()
            f.write(content)

        addFileRequest=AddFileRequest(
            filename=file.filename,
            filepath=str(filePath),
            size= len(content),
            uploaded_by=userId,
            status=FileStatus.PENDING,
            uploaded_at=datetime.now(),
            tags=tags
        )
        # admin adds already accepted files
        user = request.state.user
        if user.role==Role.ADMIN:
            addFileRequest.status=FileStatus.ACCEPTED

        return await self.repo.insert_file_with_tags(addFileRequest)
    async def get_accepted_files(self,request: Request):
        user_auth(request)
        return await self.repo.get_accepted_files()




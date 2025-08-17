import os
import secrets
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from fastapi import UploadFile
from model.fileModel import AddFileRequest, FileStatus, ChangeStatusRequest
from repository.fileRepository import FileRepository

#TODO: update path to make it correct
UPLOAD_DIR=Path("uploads")

class FileService:
    def __init__(self):
        self.repo = FileRepository()
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    async def upload_file(self,file: UploadFile, tags: list[int],userId: int):
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
        return await self.repo.insert_file_with_tags(addFileRequest)

    async def get_accepted_files(self):
        return await self.repo.get_accepted_files()

    async def change_status(self,request: ChangeStatusRequest):
        return await self.repo.change_status(request)

    async def get_all_files(self):
        return await self.repo.get_all_files()
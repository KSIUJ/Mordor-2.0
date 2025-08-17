from enum import Enum
from typing import List

from db import db
from model.fileModel import AddFileRequest
import json
class FileRepository:
    def __init__(self):
        self.db=db
    async def insert_file_with_tags(self,request: AddFileRequest):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                status_value = request.status.value if isinstance(request.status, Enum) else request.status
                await conn.execute("""
                    INSERT INTO files (name, filepath, status, size, uploaded_at, uploaded_by)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    request.filename,
                    request.filepath,
                    status_value,
                    request.size,
                    request.uploaded_at,
                    request.uploaded_by
                ))

                file_id = cursor.lastrowid

                for tag_id in request.tags:
                    cursor.execute("""
                        INSERT INTO tag_file (file_id, tag_id) VALUES (?, ?)
                    """, (file_id, tag_id))

                await conn.commit()
                conn.close()

                return {"file_id": file_id, "tags": request.tags}
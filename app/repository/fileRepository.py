from enum import Enum
from typing import List

from db import db
from model.fileModel import AddFileRequest, FileInfo, AfterUploadResponse, AcceptedFilesResponse, FileStatus, \
    ChangeStatusRequest, CommonResponse
import json
class FileRepository:
    def __init__(self):
        self.db=db
    async def insert_file_with_tags(self,request: AddFileRequest):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                status_value = request.status.value if isinstance(request.status, Enum) else request.status
                await cursor.execute("""
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

                if request.tags:
                    await cursor.executemany(
                        "INSERT INTO tag_file (file_id, tag_id) VALUES (?, ?)",
                        [(file_id, tag_id) for tag_id in request.tags]
                    )

                await conn.commit()
                conn.close()
                return AfterUploadResponse(return_code=200,file_id=file_id,tags=request.tags)

    async def get_accepted_files(self):
        """Returns basic info about accepted files to common user"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         SELECT id, name, size, uploaded_by, status
                                         FROM files
                                         WHERE status = 'accepted'
                                         """)
                    rows = await cursor.fetchall()
                    files = []
                    for row in rows:
                        files.append(FileInfo(
                            id=row[0],
                            name=row[1],
                            size=row[2],
                            uploaded_by=row[3],
                            status=FileStatus(row[4])
                        ))
                    conn.close()
                    return AcceptedFilesResponse(return_code=200, files=files)
                except Exception as e:
                    return CommonResponse(return_code=500)

    async def change_status(self,request: ChangeStatusRequest):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                    UPDATE files
                    SET status = ?
                    where id = ?
                                         """,(
                        request.status.value,
                        request.fileId
                    ))
                    await conn.commit()
                    conn.close()
                    return CommonResponse(return_code=200)
                except Exception as e:
                    return CommonResponse(return_code=500)

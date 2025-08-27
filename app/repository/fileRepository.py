from enum import Enum
from typing import List

from fastapi import HTTPException

from db import db
from model.exceptions import DatabaseError
from model.fileModel import AddFileRequest, FileInfo, FileStatus, ChangeStatusRequest, UpdateFileRequest


def process_files(rows):
    """Helper method to avoid redundant code"""
    files = []
    for row in rows:
        files.append(FileInfo(
            id=row[0],
            name=row[1],
            size=row[2],
            uploaded_by=row[3],
            status=FileStatus(row[4]),
            filepath=row[5]
        ))
    return files


class FileRepository:

    def __init__(self):
        self.db=db

    # ==================== QUERIES ====================

    async def get_file_by_id(self, fileId: int):
        """Get basic info about a file having its id"""

        async with self.db.get_connection() as conn:

            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         SELECT id, name, size, uploaded_by, status,filepath
                                         FROM files
                                         WHERE id = ?
                                         """, (fileId,))

                    row = await cursor.fetchone()

                    if not row:
                        return None

                    return FileInfo(
                        id=row[0],
                        name=row[1],
                        size=row[2],
                        uploaded_by=row[3],
                        status=FileStatus(row[4]),
                        filepath=row[5]
                    )
                except Exception as e:
                    raise DatabaseError()

    async def get_accepted_files(self):
        """Returns basic info about accepted files to common user"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         SELECT id, name, size, uploaded_by, status, filepath
                                         FROM files
                                         WHERE status = 'accepted'
                                         """)
                    rows = await cursor.fetchall()
                    files = process_files(rows)
                    conn.close()
                    return files
                except Exception as e:
                    raise DatabaseError()

    async def get_all_files(self):
        """Returns basic info about accepted files to common user"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         SELECT id, name, size, uploaded_by, status,filepath
                                         FROM files
                                         """)
                    rows = await cursor.fetchall()
                    files = process_files(rows)
                    conn.close()
                    return files
                except Exception as e:
                    raise DatabaseError()

    # =========================== UPDATES ==============================


    async def update_file(self, request: UpdateFileRequest,tags):
        """Update file metadata"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:

                    await cursor.execute("""
                                         UPDATE files
                                         SET name     = ?,
                                             filepath = ?,
                                             size     = ?
                                         WHERE id = ?
                                         """, (
                                             request.filename,
                                             request.filepath,
                                             request.size,
                                             request.id
                                         ))
                    await conn.commit()
                    if cursor.rowcount == 0:
                        raise FileNotFoundError()

                    await self.update_tags(request.id,tags)

                    conn.close()
                    return None
                except Exception as e:
                    raise DatabaseError()

    async def change_status(self, request: ChangeStatusRequest):
        """Changes status of file"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         UPDATE files
                                         SET status = ?
                                         where id = ?
                                         """, (
                                             request.status.value,
                                             request.file_id
                                         ))
                    await conn.commit()
                    conn.close()
                    return None
                except Exception as e:
                    raise DatabaseError()

    async def update_tags(self, fileId: int, tags: List[int]):
        """Update tags of file"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         DELETE
                                         FROM tag_file
                                         WHERE file_id = ?
                                         """, (fileId,))
                    await conn.commit()
                    #  Add new tags

                    if tags:
                        await cursor.executemany(
                            "INSERT INTO tag_file (file_id, tag_id) VALUES (?, ?)",
                            [(fileId, tag_id) for tag_id in tags]
                        )
                    await conn.commit()
                    conn.close()
                    return None
                except Exception as e:
                    raise DatabaseError()

    #   ========================== INSERTS ===========================

    async def insert_file_with_tags(self,request: AddFileRequest):
        """Inserts requested file"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:

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
                    return file_id
                except Exception as e:
                    raise DatabaseError()

    # ============================ DELETE ===================================\
    async def delete_file(self,fileId: int):
        """Deletes file having its id"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                        DELETE 
                                        FROM tag_file
                                        where file_id = ?
                                        """, (fileId,))
                    await conn.commit()
                    await cursor.execute("""
                                         DELETE
                                         FROM files
                                         where id = ?
                                         """, (fileId,))
                    await conn.commit()
                    conn.close()
                    return None
                except Exception as e:
                    raise DatabaseError()

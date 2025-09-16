from db import db
from model.exceptions import DatabaseError

class LimitsRepository:
    """IMPLEMENTS CHECKING IF USER CAN UPLOAD/MODIFY A FILE"""
    def __init__(self):
        self.db = db

    async def countOverflow(self,userId):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                            SELECT number_limit
                            FROM users JOIN users_limits ON users.role = users_limits.user_role
                            WHERE users.id = ?
                        """,(userId,))
                    result = await cursor.fetchone()
                    await cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM users JOIN files ON users.id = files.uploaded_by
                        WHERE files.uploaded_at > datetime('now', '-1 month')
                        """
                    )
                    count = await cursor.fetchone()
                    conn.close()
                    if count>=result:
                        return False
                    else:
                        return True
                except Exception as e:
                    raise DatabaseError()

    async def sizeOverflow(self,userId,size):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                            SELECT size_limit
                            FROM users JOIN users_limits ON users.role = users_limits.user_role
                            WHERE users.id = ?
                        """,(userId,))
                    result = await cursor.fetchone()
                    await cursor.execute(
                        """
                        SELECT SUM(files.size)
                        FROM users JOIN files ON users.id = files.uploaded_by
                        WHERE files.uploaded_at > datetime('now', '-1 month')
                        """
                    )
                    sum = await cursor.fetchone()
                    conn.close()
                    if sum+size>=result:
                        return False
                    else:
                        return True
                except Exception as e:
                    raise DatabaseError()
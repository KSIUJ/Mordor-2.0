from db import db
from model.exceptions import DatabaseError

class LimitsRepository:
    """IMPLEMENTS CHECKING IF USER CAN UPLOAD/MODIFY A FILE"""
    def __init__(self):
        self.db = db

    async def countOverflow(self, user_id, user_role):
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(
                        """
                        SELECT ul.size_limit, ul.number_limit
                        FROM users_limits ul
                        WHERE ul.user_role = ?
                        """,(user_role,))
                        
                    result = await cursor.fetchone()
                    await cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM files
                        WHERE files.uploaded_by = ?
                        AND files.uploaded_at > datetime('now', '-1 month')
                        """, (user_id,)
                        )
                    count = await cursor.fetchone()
                    if count>=result:
                        return False
                    else:
                        return True
                except Exception as e:
                    raise DatabaseError()

    async def sizeOverflow(self,user_role,size):
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
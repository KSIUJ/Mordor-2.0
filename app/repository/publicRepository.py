from db import db
from model.exceptions import DatabaseError
from model.tagModel import TagModel

class PublicRepository:
    def __init__(self):
        self.db = db
    async def get_tags(self):
        """Just tag info"""
        async with self.db.get_connection() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute("""
                                         SELECT id,name
                                         FROM tags
                                         ORDER BY name
                                         """)
                    rows = await cursor.fetchall()
                    tags = []
                    for row in rows:
                        tags.append(TagModel(
                            id=row[0],
                            name=row[1]
                        ))
                    conn.close()
                    return tags
                except Exception as e:
                    raise DatabaseError()
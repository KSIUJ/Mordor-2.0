from db import db
from pathlib import Path
from typing import Optional
import logging
from pydantic import BaseModel
import aiosqlite

class UserLimits(BaseModel):
    user_role: str
    size_limit: int = 10000000  
    number_limit: int = 20

class User(BaseModel):
    id: Optional[int] = None
    username: str
    role: str
    email: Optional[str] = None

class UserWithLimits(BaseModel):
    id: Optional[int] = None
    username: str
    role: str
    email: Optional[str] = None
    size_limit: int
    number_limit: int


class UserRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        async with self.db_connection.get_connection() as db:
            cursor : aiosqlite.Cursor = await db.execute(
                "SELECT id, username, role, email FROM users WHERE id = ?",
                (user_id,)
            )
            row = await cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    role=row[2],
                    email=row[3]
                )

            return None
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        async with self.db_connection.get_connection() as db:
            cursor : aiosqlite.Cursor = await db.execute(
                "SELECT id, username, role, email FROM users WHERE username = ?",
                (username,)
            )
            row = await cursor.fetchone()
            if row:
                return User(
                    id=row[0],
                    username=row[1],
                    role=row[2],
                    email=row[3]
                )
            return None
    
    async def get_user_with_limits(self, user_id: int) -> Optional[UserWithLimits]:
        """Get user with their role limits."""
        async with self.db_connection.get_connection() as db:
            cursor : aiosqlite.Cursor = await db.execute("""
                SELECT u.id, u.username, u.role, u.email, 
                       ul.size_limit, ul.number_limit
                FROM users u
                JOIN users_limits ul ON u.role = ul.user_role
                WHERE u.id = ?
            """, (user_id,))
            
            row = await cursor.fetchone()
            if row:
                return UserWithLimits(
                    id=row[0],
                    username=row[1],
                    role=row[2],
                    email=row[3],
                    size_limit=row[4],
                    number_limit=row[5]
                )
            return None
    
    async def get_user_with_limits_by_username(self, username: str) -> Optional[UserWithLimits]:
        """Get user with their role limits by username."""
        async with self.db_connection.get_connection() as db:
            cursor : aiosqlite.Cursor = await db.execute("""
                SELECT u.id, u.username, u.role, u.email, 
                       ul.size_limit, ul.number_limit
                FROM users u
                JOIN users_limits ul ON u.role = ul.user_role
                WHERE u.username = ?
            """, (username,))
            
            row = await cursor.fetchone()
            if row:
                 return UserWithLimits(
                    id=row[0],
                    username=row[1],
                    role=row[2],
                    email=row[3],
                    size_limit=row[4],
                    number_limit=row[5]
                )
            return None

user_repo = UserRepository(db)
import aiosqlite
import os
from typing import Optional

class DatabaseConnection:
    def __init__(self):
        self.db_path: Optional[str] = None
    
    async def connect(self):
        """Initialize database connection"""
        database_url = os.getenv("DATABASE_URL", "sqlite:///db/database.db")
        
        self.db_path = database_url.replace("sqlite://", "")
        
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            pass
    
    async def disconnect(self):
        """Close database connection (no persistent connection for SQLite)"""
        pass
    
    async def delete(self):
        os.remove(self.db_path)
    
    async def get_connection(self):
        """Get a database connection context manager"""
        if not self.db_path:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return aiosqlite.connect(self.db_path)

# Global database instance
db = DatabaseConnection()
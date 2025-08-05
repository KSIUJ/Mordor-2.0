import aiosqlite
import os
from pathlib import Path
from typing import Optional

class DatabaseConnection:
    def __init__(self):
        self.db_path: Optional[str] = None
        self._initialized = False
    
    async def connect(self):
        """Initialize database connection"""
        database_url = os.getenv("DATABASE_URL", "sqlite://./db/database.db")
        
        self.db_path = database_url.replace("sqlite://", "")
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        async with aiosqlite.connect(self.db_path) as db:
            if not await self._is_initialized(db):
                await self._run_init_scripts(db)
                self._initialized = True
    
    async def disconnect(self):
        """Close database connection (no persistent connection for SQLite)"""
        pass
    
    async def delete(self):
        os.remove(self.db_path)
        self._initialized=False
    
    def get_connection(self):
        """Get a database connection context manager"""
        if not self.db_path:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return aiosqlite.connect(self.db_path)

    async def _is_initialized(self, db: aiosqlite.Connection) -> bool:
        """Check if database is already initialized"""
        try:
            # Check if any tables exist (you can customize this check)
            cursor = await db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = await cursor.fetchall()
            return len(tables) > 0
        except Exception:
            return False

    async def _run_init_scripts(self, db: aiosqlite.Connection):
        """Execute all scripts frob db/init"""
        init_dir=Path(__file__).parent.parent / "db" / "init"

        try:
            scripts = sorted(f for f in os.listdir(init_dir) if f.endswith(".sql"))
        except OSError as e:
            print(f"Error reading init directory: {e}")
            return

        for script in scripts:
            script_path = init_dir / script
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    sql = f.read()
                    if sql.strip():  # Only execute non-empty scripts
                        await db.executescript(sql)
                        print(f"Executed script: {script}")
            except Exception as e:
                print(f"Error executing script {script}: {e}")
                raise
        await db.commit()

# Global database instance
db = DatabaseConnection()
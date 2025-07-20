from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
from db import db

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@router.get("/db")
async def database_health():
    """Database connectivity check"""
    try:
        async with db.get_connection() as conn:
            cursor = await conn.execute("SELECT 1")
            result = await cursor.fetchone()
            if result and result[0] == 1:
                return {"status": "healthy", "message": "Database connection is working"}
            else:
                raise HTTPException(status_code=503, detail="Database query returned unexpected result")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@router.post("/db/test")
async def test_database_write():
    """Test database write/read operations"""
    try:
        async with db.get_connection() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS health_test (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            test_message = f"Health check at {datetime.now().isoformat()}"
            cursor = await conn.execute(
                "INSERT INTO health_test (message) VALUES (?)",
                (test_message,)
            )
            await conn.commit()
            
            cursor = await conn.execute(
                "SELECT id, message, created_at FROM health_test ORDER BY id DESC LIMIT 1"
            )
            result = await cursor.fetchone()
            
            if result:
                return {
                    "status": "success",
                    "message": "Database write/read test passed",
                    "data": {
                        "id": result[0],
                        "message": result[1],
                        "created_at": result[2]
                    }
                }
            else:
                raise HTTPException(status_code=500, detail="Failed to read back test data")
                
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")

@router.get("/db/test")
async def get_test_data():
    """Get all test data from database"""
    try:
        async with db.get_connection() as conn:
            cursor = await conn.execute(
                "SELECT id, message, created_at FROM health_test ORDER BY id DESC LIMIT 10"
            )
            results = await cursor.fetchall()
            
            test_records = [
                {
                    "id": row[0],
                    "message": row[1], 
                    "created_at": row[2]
                }
                for row in results
            ]
            
            return {
                "status": "success",
                "count": len(test_records),
                "data": test_records
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve test data: {str(e)}")

@router.delete("/db/test")
async def clear_test_data():
    """Clear all test data"""
    try:
        async with db.get_connection() as conn:
            cursor = await conn.execute("DELETE FROM health_test")
            await conn.commit()
            
            return {
                "status": "success",
                "message": f"Cleared {cursor.rowcount} test records"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear test data: {str(e)}")

@router.get("/status", response_class=HTMLResponse)
async def health_status_page(request: Request):
    """Health status page with template"""
    # Get API status
    api_status = {"status": "healthy", "message": "API is running"}
    
    # Get database status
    try:
        async with db.get_connection() as conn:
            cursor = await conn.execute("SELECT 1")
            result = await cursor.fetchone()
            if result and result[0] == 1:
                db_status = {"status": "healthy", "message": "Database connection is working"}
            else:
                db_status = {"status": "unhealthy", "message": "Database query failed"}
    except Exception as e:
        db_status = {"status": "unhealthy", "message": "Database connection failed", "error": str(e)}
    
    return templates.TemplateResponse("health/status.html", {
        "request": request,
        "api_status": api_status,
        "db_status": db_status,
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "environment": os.getenv("ENVIRONMENT", "development")
    })
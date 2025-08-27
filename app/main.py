from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from router.health import router as health_router
from router.testEndpoints import router as test_router
from router.admin.fileManagement import router as admin_file_router
from router.user.fileManagement import router as user_file_router
from db import db
import logging
import asyncio
from services.authservice import AuthMiddleware, Role
from parser.parser import parseExpression
from templates import patch_templates

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")
patch_templates()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


from typing import Dict, List
# Route configuration: Role -> List of routes
# Needs to include full routes but every route under the route included will also require the highest level the route included in
ROLE_ROUTES: Dict[Role, List[str]] = {
    Role.PUBLIC: ["/"],
    Role.USER: ["/test/auth/user", "/health"],
    Role.MANAGER: ["/test/auth/manager"],
    Role.ADMIN: ["/test/auth/admin"],
}
#Add Role Middleware
app.add_middleware(AuthMiddleware, config = {
    "ROLE_ROUTES" : ROLE_ROUTES,                                     
                                             })

# Include routers
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(health_router)
app.include_router(test_router)
app.include_router(admin_file_router)
app.include_router(user_file_router)
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup with retry logic"""
    max_retries = 10
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            await db.connect()
            logging.info("Database connection established successfully")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logging.warning(f"Database connection attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, 30)  # Exponential backoff, max 30 seconds
            else:
                logging.error(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    await db.disconnect()
    # !!!!!!!!!!!!!👎👎👎👎 USE FOR TESTING
    await db.delete()

@app.get("/")
async def root():
    return {"message": "Hello, World4!"}

@app.get("/placeholder_search")
async def placeholder():
    return FileResponse("static/placeholder_search.html")

@app.get("/api/files")
async def api_files(q: str = Query("", max_length=250)):
    try:
        if not q:
            return []
        
        q = q.strip()
        
        ast = parseExpression(q)
        results = await db.get_files_by_tags(ast)
        return results
    
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=f"Invalid syntax: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.exception(f"Server error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
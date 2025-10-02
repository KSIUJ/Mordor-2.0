from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request
from router.health import router as health_router
from router.testEndpoints import router as test_router
from router.admin.fileManagement import router as admin_file_router
from router.user.fileManagement import router as user_file_router
from router.user.tagRouter import router as tag_router
from router.upload import router as upload_router
from router.update import router as update_router
from router.User import router as user_router
from db import db
from repository.user_repository import user_repo
import logging
import asyncio
# from services.authservice import AuthMiddleware, Role
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


from fastapi import FastAPI, Request
from ksi_oidc_fastapi.auth_middleware import AuthMiddleware
from ksi_oidc_fastapi.auth_router import router as auth_router
from ksi_oidc_fastapi.models import Role
from typing import Dict, List
# Route configuration: Role -> List of routes
# Needs to include full routes but every route under the route included will also require the highest level the route included in
from model.user import Role as CurRole
Role = CurRole
ROLE_ROUTES: Dict[Role, List[str]] = {
    Role.PUBLIC: ["/", "/auth/login", "/auth/callback", "/auth/logout"],
    Role.USER: ["/profile", "/test/auth/user", "/health","/user/upload","/user/file", "/user/files","/user/tags","/update/","/upload/", "/auth/protected"],
    Role.ADMIN: ["/test/auth/admin","/admin/upload","/admin/file", "/admin/all_files","/admin/change_status", "/auth/admin"],
    Role.MANAGER: ["/manager"],
}
#Add Role Middleware
# app.add_middleware(AuthMiddleware, config = {
#     "ROLE_ROUTES" : ROLE_ROUTES,                                     
#                                              })

app.add_middleware(
  AuthMiddleware,
  user_repository_instance=user_repo,
  session_cookie_name="session_id",
  session_cookie_httponly=True,
  session_cookie_secure=True,
  route_configuration=ROLE_ROUTES,
  login_redirect_path="/auth/login",
  role_hierarchy=[Role.PUBLIC, Role.USER, Role.MANAGER, Role.ADMIN],
)



# Include routers
app.include_router(auth_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(health_router)
# app.include_router(test_router)
app.include_router(admin_file_router)
app.include_router(user_file_router)
app.include_router(tag_router)
app.include_router(upload_router)
app.include_router(update_router)
app.include_router(user_router)

app.include_router(tag_router)
app.include_router(upload_router)
app.include_router(update_router)


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


from repository.user_repository import user_repo
from repository.fileRepository import file_repo
from model.user import UserWithLimits
from model.fileModel import FileInfo, FileStatus
from typing import List
import logging

def format_file_size(size_bytes: int) -> str:
    """Convert bytes to be in a readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


# async def root():
#     return {"message": "Hello, World4!"}
@app.get("/")
async def main(request: Request):
    files : List[FileInfo] = await file_repo.get_accepted_files()
    for i, value in enumerate(files):
        files[i].status = files[i].status.value
        files[i].name = f"{files[i].name}.{files[i].filepath.split('.')[1]}"
    return templates.TemplateResponse("main.html", {
        "request": request,
        "files" : files,
        "format_file_size": format_file_size
        })

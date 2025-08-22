from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse
from services.authservice import Role
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def auth_home(request: Request):
    return templates.TemplateResponse("authtesting/authtest.html", {
        "request": request
        })

@router.get("/public")
async def public_route(request: Request):
    """Public endpoint accessible to all."""
    user = request.state.user
    return {"message": f"This is a public endpoint, {user.username} with role {user.role}"}

@router.get("/user")
async def user_route(request: Request):
    """Endpoint accessible to USER, MANAGER, and ADMIN users."""
    user = request.state.user
    return {"message": f"Welcome, {user.username} with role {user.role}"}

@router.get("/manager")
async def manager_route(request: Request):
    """Endpoint accessible to MANAGER and ADMIN users."""
    user = request.state.user
    return {"message": f"Welcome, manager {user.username}"}

@router.get("/admin")
async def admin_route(request: Request):
    """Endpoint accessible only to ADMIN users."""
    user = request.state.user
    return {"message": f"Welcome, admin {user.username}"}

@router.get("/random")
async def random_route(request: Request):
    """Sample unlisted route accessible to USER, MANAGER, and ADMIN users."""
    user = request.state.user
    return {"message": f"Random route accessed by {user.username} with role {user.role}"}

@router.get("/login")
async def login():
    role = "USER"
    response = JSONResponse(content={"message": f"Role set to {role}"})
    response.set_cookie(key="X-Role", value=role)
    return response

@router.get("/logout")
async def logout():
    print(">>>")
    response = JSONResponse(content={"message": f"Logged out"})
    response.delete_cookie(key="X-Role")
    return response


# Helper endpoint to set mock role cookie (for testing)
@router.get("/set-role/{role}")
async def set_role_cookie(role: str, response: JSONResponse):
    """
    Helper endpoint to set the X-Role cookie for testing.
    
    Args:
        role: Role to set (USER, ADMIN, MANAGER).
        response: JSONResponse to set the cookie.
    
    Returns:
        JSONResponse: Confirmation message with the cookie set.
    """
    role = role.upper()
    if role == Role.PUBLIC:
        response = JSONResponse(content={"message": f"Logged out"})
        response.delete_cookie(key="X-Role")
    elif role not in [Role.USER, Role.ADMIN, Role.MANAGER]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Use USER, ADMIN, or MANAGER"
        )
    else:
        response = JSONResponse(content={"message": f"Role set to {role}"})
        response.set_cookie(key="X-Role", value=role)
    return response

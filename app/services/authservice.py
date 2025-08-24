from enum import Enum
from pydantic import BaseModel
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from repositories.user_repository import User, user_repo
import logging

# Define user roles
class Role(str, Enum):
    PUBLIC = "PUBLIC"  # No authentication required
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

# User model to mock authentication

class AuthService:
    """Mock authentication service for development using cookie role simulation."""

    COOKIE_ROLE_KEY = "X-Role"
    role_hierarchy = [Role.PUBLIC, Role.USER, Role.MANAGER, Role.ADMIN]
    
    def _normalize_path(self, path: str) -> str:
        """Remove trailing slash except for root path."""
        if path == "/" or not path:
            return "/"
        return path.rstrip("/")
    # !!!! ❗❗❗❗
    # Later change get_user_from_cookie to new fucntion which will be using OPENIDCONNECT(get_user_from_token??)
    async def get_user_from_cookie(self, request: Request) -> User:
        """Get user from cookie or return PUBLIC user."""
        role = request.cookies.get(self.COOKIE_ROLE_KEY)
        if not role:
            return User(username="mock_public_user", role=Role.PUBLIC)
        
        try:
            role = Role(role.upper())
        except ValueError:
            return User(username="mock_public_user", role=Role.PUBLIC)
        
        username = f"{role.lower()}_dummy"
        user = await user_repo.get_user_by_username(username=username)
        return user

    def is_path_allowed(self, path: str, user_role: Role, ROLE_ROUTES : dict) -> bool:
        """Check if user role can access the path."""
        normalized_path = self._normalize_path(path)
        user_level = self.role_hierarchy.index(user_role)
        
        # Check if the path starts with any route from higher roles
        for i in range(user_level + 1, len(self.role_hierarchy)):
            higher_role = self.role_hierarchy[i]
            for route in ROLE_ROUTES.get(higher_role, []):
                normalized_route = self._normalize_path(route)
                if normalized_path.startswith(normalized_route):
                    return False
        
        return True

auth_service = AuthService()

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware that blocks access to higher role routes."""
    def __init__(self,app, config):
        super().__init__(app)
        self.ROLE_ROUTES = config["ROLE_ROUTES"]
        
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        user = await auth_service.get_user_from_cookie(request)
        request.state.user = user
        
        if not auth_service.is_path_allowed(path, user.role, self.ROLE_ROUTES):
            if user.role == Role.PUBLIC:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content="User not authorized"
                )
            return  JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content="Insufficient role permissions"
            )
        response = await call_next(request)
        return response
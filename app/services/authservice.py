from enum import Enum
from typing import Dict, List
from pydantic import BaseModel
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

# Define user roles
class Role(str, Enum):
    PUBLIC = "PUBLIC"  # No authentication required
    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"

# Route configuration: Role -> List of routes
# Needs to include full routes but every route under the route included will also require the highest level the route included in
ROLE_ROUTES: Dict[Role, List[str]] = {
    Role.PUBLIC: ["/"],
    Role.USER: ["/test/auth/user", "/health"],
    Role.MANAGER: ["/test/auth/manager"],
    Role.ADMIN: ["/test/auth/admin"],
}

# User model to mock authentication
class User(BaseModel):
    username: str
    role: Role

class AuthService:
    """Mock authentication service for development using cookie role simulation."""
    
    COOKIE_ROLE_KEY = "X-Role"
    
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
        
        username = f"mock_{role.lower()}_user"
        return User(username=username, role=role)

    def is_path_allowed(self, path: str, user_role: Role) -> bool:
        """Check if user role can access the path."""
        normalized_path = self._normalize_path(path)
        role_hierarchy = [Role.PUBLIC, Role.USER, Role.MANAGER, Role.ADMIN]
        user_level = role_hierarchy.index(user_role)
        
        # Check if the path starts with any route from higher roles
        for i in range(user_level + 1, len(role_hierarchy)):
            higher_role = role_hierarchy[i]
            for route in ROLE_ROUTES.get(higher_role, []):
                normalized_route = self._normalize_path(route)
                if normalized_path.startswith(normalized_route):
                    return False
        
        return True

auth_service = AuthService()

async def auth_middleware(request: Request, call_next):
    """Middleware that blocks access to higher role routes."""
    path = request.url.path
    user = await auth_service.get_user_from_cookie(request)
    request.state.user = user
    
    if not auth_service.is_path_allowed(path, user.role):
        return  JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Insufficient role permissions"
            
        )
    
    response = await call_next(request)
    return response

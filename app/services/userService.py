from fastapi import Request, HTTPException
from repository.user_repository import UserRepository
from services.authservice import User, Role


# === authorisation ===
def admin_auth(request: Request):
    """For functions that require admin access"""
    user = request.state.user
    if user.role not in [Role.ADMIN]:
        raise PermissionError

# === UserService class ===
class UserService:
    def __init__(self):
        self.repo = UserRepository()
    
    # === Admin operations ===
    async def get_all_users(self, request: Request):
        admin_auth(request)
        return await self.repo.get_all_users()

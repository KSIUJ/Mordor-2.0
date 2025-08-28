from pydantic import BaseModel
from typing import Optional
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
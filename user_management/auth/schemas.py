from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr

class UserRead(schemas.BaseUser[int]):
    username: str
    full_name: Optional[str]

class UserCreate(schemas.BaseUserCreate):
    username: str
    full_name: Optional[str]

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    full_name: Optional[str]

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    id: str = Field(..., description="ID người dùng")
    email: str = Field(..., description="Email đăng nhập")
    full_name: str = Field(..., description="Họ tên đầy đủ")
    role: UserRole = Field(default=UserRole.USER, description="Vai trò người dùng")
    avatar_url: Optional[str] = Field(default=None, description="URL ảnh đại diện")
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from app.schemas.v1.role import RoleOut


class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role_id: int  # Reference to roles table

class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "full_name": "John Doe",
                "email": "john@example.com",
                "role_id": 1,  # Reference to a valid role
                "password": "strongpassword123"
            }
        }
    }

class UserOut(UserBase):
    id: int
    username: str
    full_name: str
    email: EmailStr
    role: RoleOut  # Show full role info in output

    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    username: str
    password: str

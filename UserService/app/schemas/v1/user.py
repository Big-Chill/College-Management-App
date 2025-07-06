from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    role: str  # e.g., student, faculty, hod

class UserCreate(UserBase):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "john_doe",
                "full_name": "John Doe",
                "email": "john@example.com",
                "role": "student",
                "password": "strongpassword123"
            }
        }
    }

class UserOut(UserBase):
    id: int

    model_config = {
        "from_attributes": True  # For SQLAlchemy ORM compatibility in Pydantic v2
    }

class UserLogin(BaseModel):
    username: str
    password: str

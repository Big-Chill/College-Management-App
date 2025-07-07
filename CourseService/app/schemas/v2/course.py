from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

class CourseOut(CourseBase):
    id: str
    class Config:
        orm_mode = True
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ----- Teacher Schemas -----
class TeacherBase(BaseModel):
    name: str
    email: EmailStr

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int
    class Config:
        orm_mode = True

# ----- Subject Schemas -----
class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    teacher_ids: List[int] = []

class SubjectOut(SubjectBase):
    id: int
    teachers: List[TeacherOut] = []
    class Config:
        orm_mode = True

# ----- Course Schemas -----
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    subjects: List[SubjectCreate] = []

class CourseOut(CourseBase):
    id: int
    subjects: List[SubjectOut] = []
    class Config:
        orm_mode = True

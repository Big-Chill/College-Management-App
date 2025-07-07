from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.v1.id_generator import generate_primary_id

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, default=lambda: generate_primary_id("course"))
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    subjects = relationship("Subject", back_populates="course", cascade="all, delete-orphan")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(String, primary_key=True, default=lambda: generate_primary_id("subject"))
    name = Column(String, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="subjects")
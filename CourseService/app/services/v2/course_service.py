from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.v1.course import Course

class CourseService:
    @staticmethod
    def create_course(db: Session, name: str, description: str):
        # Check for existing course
        existing = db.query(Course).filter(Course.name == name).first()
        if existing:
            raise ValueError("Course already exists")

        course = Course(name=name, description=description)
        db.add(course)
        try:
            db.commit()
            db.refresh(course)
        except IntegrityError:
            db.rollback()
            raise ValueError("Integrity error creating course")

        return course

    @staticmethod
    def list_courses(db: Session):
        return db.query(Course).all()

    @staticmethod
    def get_course(db: Session, course_id: int):
        return db.query(Course).filter(Course.id == course_id).first()
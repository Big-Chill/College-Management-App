from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.v1.course import Course, Subject, Teacher

class CourseService:
    @staticmethod
    def create_course(db: Session, name: str, description: str, subjects_data: list):
        # Check for existing course
        existing = db.query(Course).filter(Course.name == name).first()
        if existing:
            raise ValueError("Course already exists")
        subjects = []
        for subj in subjects_data:
            teachers = db.query(Teacher).filter(Teacher.id.in_(subj["teacher_ids"])).all()
            subject = Subject(name=subj["name"], teachers=teachers)
            subjects.append(subject)
        course = Course(name=name, description=description, subjects=subjects)
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

class SubjectService:
    @staticmethod
    def create_subject(db: Session, name: str, teacher_ids: list):
        teachers = db.query(Teacher).filter(Teacher.id.in_(teacher_ids)).all()
        subject = Subject(name=name, teachers=teachers)
        db.add(subject)
        db.commit()
        db.refresh(subject)
        return subject

    @staticmethod
    def list_subjects(db: Session):
        return db.query(Subject).all()

class TeacherService:
    @staticmethod
    def create_teacher(db: Session, name: str, email: str):
        existing = db.query(Teacher).filter(Teacher.email == email).first()
        if existing:
            raise ValueError("Teacher already exists")
        teacher = Teacher(name=name, email=email)
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        return teacher

    @staticmethod
    def list_teachers(db: Session):
        return db.query(Teacher).all()

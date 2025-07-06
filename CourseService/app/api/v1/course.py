from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.v1.course import CourseCreate, CourseOut, SubjectCreate, SubjectOut, TeacherCreate, TeacherOut
from app.services.v1.course_service import CourseService, SubjectService, TeacherService
from app.dependencies.v1.course import get_current_user, require_role

router = APIRouter()

# ----- Course Endpoints -----

@router.post("/courses/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["hod"]))
):
    try:
        course = CourseService.create_course(
            db,
            name=course_in.name,
            description=course_in.description,
            subjects_data=[subj.dict() for subj in course_in.subjects]
        )
        return course
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/courses/", response_model=list[CourseOut])
def list_courses(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return CourseService.list_courses(db)

@router.get("/courses/{course_id}", response_model=CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    course = CourseService.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

# ----- Subject Endpoints -----

@router.post("/subjects/", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_in: SubjectCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["hod", "faculty"]))
):
    subject = SubjectService.create_subject(
        db,
        name=subject_in.name,
        teacher_ids=subject_in.teacher_ids
    )
    return subject

@router.get("/subjects/", response_model=list[SubjectOut])
def list_subjects(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return SubjectService.list_subjects(db)

# ----- Teacher Endpoints -----

@router.post("/teachers/", response_model=TeacherOut, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher_in: TeacherCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["hod"]))
):
    try:
        teacher = TeacherService.create_teacher(
            db,
            name=teacher_in.name,
            email=teacher_in.email
        )
        return teacher
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/teachers/", response_model=list[TeacherOut])
def list_teachers(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return TeacherService.list_teachers(db)

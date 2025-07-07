from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.v2.course import CourseBase, CourseOut
from app.services.v2.course_service import CourseService
from app.dependencies.v1.course import get_current_user, require_role

router = APIRouter()

@router.post("/courses/", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: CourseBase,
    db: Session = Depends(get_db),
    user=Depends(require_role(["hod","owner"]))
):
    try:
        course = CourseService.create_course(
            db,
            name=course_in.name,
            description=course_in.description
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

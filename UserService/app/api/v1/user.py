from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.v1.user import get_current_user
from sqlalchemy import or_
from app.schemas.v1.user import UserCreate, UserOut
from app.models.v1.user import User
from app.core.database import get_db
from app.core.security import hash_password
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if username or email already exists
    user = db.query(User).filter(
        or_(
            User.username == user_in.username,
            User.email == user_in.email
        )
    ).first()
    if user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    # Hash password and create user
    hashed_pw = hash_password(user_in.password)
    db_user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed_pw,
        role=user_in.role
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already registered")
    return db_user

@router.get("/me", response_model=UserOut)
def get_current_user_route(current_user: User = Depends(get_current_user)):
    return current_user

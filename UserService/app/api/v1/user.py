from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.dependencies.v1.user import get_current_user, require_role
from app.schemas.v1.user import UserCreate, UserOut
from app.models.v1.user import User
from app.models.v1.role import Role
from app.core.database import get_db
from app.core.security import hash_password

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
    # Check if role_id exists
    role = db.query(Role).filter(Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role does not exist")
    # Hash password and create user
    hashed_pw = hash_password(user_in.password)
    db_user = User(
        username=user_in.username,
        full_name=user_in.full_name,
        email=user_in.email,
        hashed_password=hashed_pw,
        role_id=user_in.role_id  # Use role_id, not role string
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

@router.get("/users", response_model=list[UserOut])
def get_all_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["owner", "admin"]))  # Only owner/admin can view all users
):
    users = db.query(User).all()
    return users
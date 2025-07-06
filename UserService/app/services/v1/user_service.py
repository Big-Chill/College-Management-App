from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from app.models.v1.user import User
from app.models.v1.role import Role
from app.schemas.v1.user import UserCreate
from app.core.security import hash_password, verify_password

class UserService:
    @staticmethod
    def create_user(db: Session, user_in: UserCreate):
        # Check if username or email already exists
        existing = db.query(User).filter(
            or_(User.username == user_in.username, User.email == user_in.email)
        ).first()
        if existing:
            raise ValueError("Username or email already registered")
        # Check if role_id exists
        role = db.query(Role).filter(Role.id == user_in.role_id).first()
        if not role:
            raise ValueError("Role does not exist")
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
            raise ValueError("Username or email already registered")
        return db_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = db.query(User).filter(
            or_(User.username == username, User.email == username)
        ).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

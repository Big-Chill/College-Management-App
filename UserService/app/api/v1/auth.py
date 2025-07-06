from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models.v1.user import User
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.v1.user import UserOut
from app.schemas.v1.token import Token  # Define this schema for JWT output

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        or_(
            User.username == form_data.username,
            User.email == form_data.username
        )
    ).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token({"sub": user.username, "role": user.role.name})
    return {"access_token": token, "token_type": "bearer"}

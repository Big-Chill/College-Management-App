from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.v1.role import RoleCreate, RoleOut
from app.models.v1.role import Role
from app.dependencies.v1.user import require_role

router = APIRouter()

@router.post("/roles/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
    role_in: RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Owner"]))  # Only owner can create roles
):
    existing = db.query(Role).filter(Role.name == role_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(name=role_in.name, description=role_in.description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

@router.get("/roles/", response_model=list[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["Owner", "Admin"]))  # Owner and admin can view roles
):
    return db.query(Role).all()

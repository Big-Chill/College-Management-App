import sys
import os
from dotenv import load_dotenv

# Ensure app modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(dotenv_path=env_path)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, Base, engine
from app.models.v1.role import Role
from app.models.v1.user import User
from app.core.security import hash_password

OWNER_ROLE_NAME = "owner"
OWNER_USERNAME = "Admin"
OWNER_EMAIL = "admin@cms.com"
OWNER_PASSWORD = "admin123"  # Change after first login!

def seed_owner():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        # 1. Create owner role if it doesn't exist
        owner_role = db.query(Role).filter(Role.name == OWNER_ROLE_NAME).first()
        if not owner_role:
            owner_role = Role(name=OWNER_ROLE_NAME, description="Superuser/Owner role")
            db.add(owner_role)
            db.commit()
            db.refresh(owner_role)
            print(f"Created role: {OWNER_ROLE_NAME}")
        else:
            print(f"Role '{OWNER_ROLE_NAME}' already exists.")

        # 2. Reset (delete) owner user if it exists
        owner_user = db.query(User).filter(User.username == OWNER_USERNAME).first()
        if owner_user:
            db.delete(owner_user)
            db.commit()
            print(f"Existing owner user '{OWNER_USERNAME}' deleted.")

        # 3. Create new owner user
        hashed_pw = hash_password(OWNER_PASSWORD)
        owner_user = User(
            username=OWNER_USERNAME,
            full_name="Owner",
            email=OWNER_EMAIL,
            hashed_password=hashed_pw,
            role_id=owner_role.id
        )
        db.add(owner_user)
        db.commit()
        db.refresh(owner_user)
        print(f"Created owner user: {OWNER_USERNAME} (email: {OWNER_EMAIL}, password: {OWNER_PASSWORD})")

    finally:
        db.close()

if __name__ == "__main__":
    seed_owner()

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.common.v1.id_generator import generate_primary_id
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: generate_primary_id("user"), index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role_id = Column(String, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role")

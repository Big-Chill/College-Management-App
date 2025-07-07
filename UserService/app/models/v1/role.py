from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.common.v1.id_generator import generate_primary_id

class Role(Base):
    __tablename__ = "roles"
    id = Column(String, primary_key=True, default=generate_primary_id("role"), index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

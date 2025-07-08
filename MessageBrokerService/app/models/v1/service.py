from sqlalchemy import Column, Integer, String
from app.core.database import Base
from app.common.v1.id_generator import generate_primary_id

class RegisteredService(Base):
    __tablename__ = "registered_services"

    id = Column(String, primary_key=True, default=lambda: generate_primary_id("service"), index=True)
    service_name = Column(String, unique=True, nullable=False)
    refresh_token = Column(String, nullable=False)

from pydantic import BaseModel
from typing import Dict, Any

class RegisterRequest(BaseModel):
    service_name: str

class RegisterResponse(BaseModel):
    service: str
    access_token: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    service: str
    access_token: str
    refresh_token: str

class PublishPayload(BaseModel):
    event: str
    data: Dict[str, Any]
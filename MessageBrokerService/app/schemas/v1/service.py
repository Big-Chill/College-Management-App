from pydantic import BaseModel

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

from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Any, Optional
from app.core.config import settings
from fastapi import Header, HTTPException
from jose import JWTError

def create_access_token(
    service_name: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": service_name, "exp": expire}
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Any:
    """Decode a JWT token and return the payload, or raise JWTError."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise e



def verify_token(authorization: str = Header(...)) -> str:
    """
    Extracts and verifies a JWT token from the Authorization header.
    Returns the 'sub' (service_name) if valid.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = authorization.split(" ")[1]

    try:
        payload = decode_access_token(token)
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

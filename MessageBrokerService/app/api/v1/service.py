from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.v1.service import RegisteredService
from app.schemas.v1.service import (
    RegisterRequest,
    RegisterResponse,
    RefreshRequest,
    RefreshResponse
)
from app.core.security import create_access_token
from app.core.security import verify_token
from app.services.v1.publisher_service import PublisherService
import secrets
from app.schemas.v1.service import PublishPayload

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register_service(payload: RegisterRequest, db: Session = Depends(get_db)):
    service = db.query(RegisteredService).filter_by(service_name=payload.service_name).first()

    if service:
        access_token = create_access_token(service.service_name)
        return RegisterResponse(
            service=service.service_name,
            access_token=access_token,
            refresh_token=service.refresh_token
        )

    refresh_token = secrets.token_hex(64)
    new_service = RegisteredService(service_name=payload.service_name, refresh_token=refresh_token)
    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    access_token = create_access_token(new_service.service_name)
    return RegisterResponse(
        service=new_service.service_name,
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh_token(payload: RefreshRequest, db: Session = Depends(get_db)):
    service = db.query(RegisteredService).filter_by(refresh_token=payload.refresh_token).first()

    if not service:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    new_refresh_token = secrets.token_hex(64)
    service.refresh_token = new_refresh_token
    db.commit()

    access_token = create_access_token(service.service_name)

    return RefreshResponse(
        service=service.service_name,
        access_token=access_token,
        refresh_token=new_refresh_token
    )


@router.post("/publish")
def publish_message(
    payload: PublishPayload,
    service_name: str = Depends(verify_token)
):
    try:
        publisher = PublisherService()
        publisher.publish(payload.dict())
        return {"status": "message published", "by": service_name, "event": payload.event, "data": payload.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {e}")

@router.get("/all_services")
def get_all_services(db: Session = Depends(get_db)):
    services = db.query(RegisteredService).all()
    return [{"serviceId": service.id, "serviceName": service.service_name} for service in services]

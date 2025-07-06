from fastapi import FastAPI
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import user, auth, role

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS settings (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned routers
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(role.router, prefix=f"{settings.API_V1_STR}/roles", tags=["roles"])

# Health check endpoint
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}


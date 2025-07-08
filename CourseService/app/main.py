from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api.v2 import course  # Make sure __init__.py imports the router
from app.models.v2 import course as course_models  # Ensure models are registered

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"/openapi.json",
    root_path="/course_service"  # Adjust if needed
)

# CORS middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend domain in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the versioned course router
app.include_router(course.router, prefix=f"{settings.API_STR}", tags=["courses"])

# Health check endpoint
@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

from fastapi import APIRouter
from src.api.routes.auth_routes import router as auth_router
from src.api.routes.triage_routes import router as triage_router
from src.api.routes.doctor_routes import router as doctor_router
from src.api.routes.appointment_routes import router as appointment_router
from src.api.routes.lab_routes import router as lab_router
from src.api.routes import profile

# Initialize the main API router for Version 1
api_v1_router = APIRouter(prefix="/api/v1")

# Register all module-specific routers under the api_v1_router
api_v1_router.include_router(auth_router)
api_v1_router.include_router(triage_router)
api_v1_router.include_router(doctor_router)
api_v1_router.include_router(appointment_router)
api_v1_router.include_router(lab_router)
api_v1_router.include_router(profile.router)
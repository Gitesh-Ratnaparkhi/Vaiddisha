# src/api/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from src.services.auth_service import register_patient, register_doctor, login_user, confirm_terms_acceptance
from src.security import auth_rate_limiter

router = APIRouter(prefix="/auth", tags=["1. Authentication & Users"])

class PatientRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    gender: str = "Unspecified"
    age: int = 0
    country: str = ""
    state: str = ""
    city: str = ""
    postal_code: str = ""
    phone: str = ""
    language: str = "English"
    conditions: str = "None"
    surgeries: str = "None"
    allergies: str = "None"

class DoctorRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str
    speciality: str
    qualification: str = ""
    experience: str = ""
    hospital: str = ""
    country: str = ""
    state: str = ""
    city: str = ""
    postal_code: str = ""
    phone: str = ""
    fee: str = ""
    description: str = ""

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TermsAcceptRequest(BaseModel):
    email: EmailStr

@router.post("/register/patient", status_code=status.HTTP_201_CREATED)
def api_register_patient(req: PatientRegisterRequest):
    msg = register_patient(
        email=req.email, password=req.password, name=req.name, gender=req.gender,
        age=req.age, country=req.country, state=req.state, city=req.city,
        postal_code=req.postal_code, phone=req.phone, language=req.language,
        conditions=req.conditions, surgeries=req.surgeries, allergies=req.allergies
    )
    if "failed" in msg.lower() or "already" in msg.lower() or "⚠️" in msg or "❌" in msg:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}

@router.post("/register/doctor", status_code=status.HTTP_201_CREATED)
def api_register_doctor(req: DoctorRegisterRequest):
    msg = register_doctor(
        email=req.email, password=req.password, name=req.name, speciality=req.speciality,
        qualification=req.qualification, experience=req.experience, hospital=req.hospital,
        country=req.country, state=req.state, city=req.city, postal_code=req.postal_code,
        phone=req.phone, fee=req.fee, description=req.description
    )
    if "failed" in msg.lower() or "already" in msg.lower() or "⚠️" in msg or "❌" in msg:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}

@router.post("/login")
def api_login(req: LoginRequest):
    if not auth_rate_limiter.is_allowed(req.email.lower()):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please wait a minute.")
    
    success, msg, user_session = login_user(req.email, req.password)
    if not success:
        raise HTTPException(status_code=401, detail=msg)
    return {"status": "success", "message": msg, "session": user_session}

@router.post("/terms/accept")
def api_accept_terms(req: TermsAcceptRequest):
    success, msg = confirm_terms_acceptance(req.email)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}
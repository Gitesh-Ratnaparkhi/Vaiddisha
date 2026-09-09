# backend/src/api/routes/profile.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from src.repositories.database import get_db_connection

router = APIRouter(prefix="/profile", tags=["Profile"])

class PatientProfileUpdate(BaseModel):
    email: str
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    language: Optional[str] = "English"
    conditions: Optional[str] = None
    surgeries: Optional[str] = None
    allergies: Optional[str] = None

class DoctorProfileUpdate(BaseModel):
    email: str
    name: str
    speciality: str
    qualification: Optional[str] = None
    experience: Optional[str] = None
    hospital: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    fee: Optional[str] = None
    description: Optional[str] = None

@router.get("/get")
def get_user_profile(email: str, role: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if role.lower() == "doctor":
        cursor.execute("SELECT * FROM doctors WHERE email = %s;", (email,))
        profile = cursor.fetchone()
    else:
        cursor.execute("SELECT * FROM patients WHERE email = %s;", (email,))
        profile = cursor.fetchone()
        
    cursor.close()
    conn.close()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"status": "success", "profile": profile}

@router.post("/update/patient")
def update_patient_profile(data: PatientProfileUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO patients (email, name, gender, age, country, state, city, postal_code, phone, language, conditions, surgeries, allergies)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
            name = EXCLUDED.name,
            gender = EXCLUDED.gender,
            age = EXCLUDED.age,
            country = EXCLUDED.country,
            state = EXCLUDED.state,
            city = EXCLUDED.city,
            postal_code = EXCLUDED.postal_code,
            phone = EXCLUDED.phone,
            language = EXCLUDED.language,
            conditions = EXCLUDED.conditions,
            surgeries = EXCLUDED.surgeries,
            allergies = EXCLUDED.allergies;
    """, (
        data.email, data.name, data.gender, data.age, data.country, 
        data.state, data.city, data.postal_code, data.phone, 
        data.language, data.conditions, data.surgeries, data.allergies
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "success", "message": "Patient profile updated successfully"}

@router.post("/update/doctor")
def update_doctor_profile(data: DoctorProfileUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors (email, name, speciality, qualification, experience, hospital, country, state, city, postal_code, phone, fee, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
            name = EXCLUDED.name,
            speciality = EXCLUDED.speciality,
            qualification = EXCLUDED.qualification,
            experience = EXCLUDED.experience,
            hospital = EXCLUDED.hospital,
            country = EXCLUDED.country,
            state = EXCLUDED.state,
            city = EXCLUDED.city,
            postal_code = EXCLUDED.postal_code,
            phone = EXCLUDED.phone,
            fee = EXCLUDED.fee,
            description = EXCLUDED.description;
    """, (
        data.email, data.name, data.speciality, data.qualification, data.experience,
        data.hospital, data.country, data.state, data.city, data.postal_code,
        data.phone, data.fee, data.description
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "success", "message": "Doctor profile updated successfully"}
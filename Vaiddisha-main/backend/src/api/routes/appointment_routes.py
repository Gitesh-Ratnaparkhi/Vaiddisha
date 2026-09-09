# src/api/routes/appointment_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from src.services.appointment_service import (
    SLOT_OPTIONS,
    book_new_appointment, 
    fetch_patient_appointments, 
    fetch_doctor_appointment_requests, 
    update_appointment_status
)
import pandas as pd

router = APIRouter(prefix="/appointments", tags=["4. Appointments & Scheduling"])


def _frontend_appointment(record: dict) -> dict:
    """Normalize database appointment names for the React client."""
    source = dict(record)
    normalized = {
        "id": source.get("id", source.get("ID", "")),
        "doctor_name": source.get("doctor_name", source.get("Doctor", "")),
        "doctor_email": source.get("doctor_email", ""),
        "patient_name": source.get("patient_name", source.get("Patient Name", "")),
        "patient_email": source.get("patient_email", source.get("Email", "")),
        "date": source.get("date", source.get("Date", source.get("appointment_date", ""))),
        "slot": source.get("slot", source.get("Slot", source.get("time_slot", ""))),
        "reason": source.get("reason", source.get("Reason", "")),
        "status": source.get("status", source.get("Status", "Pending")),
        "created_at": source.get("created_at", source.get("Requested At", "")),
    }
    return normalized

class BookAppointmentRequest(BaseModel):
    patient_email: EmailStr
    doctor_info_str: str  # Format: "Dr. Name | Speciality | City | email@example.com"
    date: str             # "YYYY-MM-DD"
    slot: str             # e.g. "10:00 AM - 10:30 AM"
    reason: str = ""

class UpdateStatusRequest(BaseModel):
    appointment_id: int
    new_status: str       # "Confirmed" | "Rejected" | "Completed"
    doctor_email: EmailStr

@router.get("/slots")
def api_get_available_slots():
    """Returns supported time slot options."""
    return {"slots": SLOT_OPTIONS}

@router.post("/book")
def api_book_appointment(req: BookAppointmentRequest):
    user_session = {"email": req.patient_email, "role": "Patient", "logged_in": True}
    msg = book_new_appointment(
        patient_session=user_session,
        doctor_selection=req.doctor_info_str,
        appointment_date=req.date,
        time_slot=req.slot,
        reason=req.reason
    )
    if "⚠️" in msg or "❌" in msg:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}

@router.get("/patient/{patient_email}")
def api_get_patient_appointments(patient_email: str):
    user_session = {"email": patient_email, "role": "Patient"}
    df = fetch_patient_appointments(user_session)
    records = [_frontend_appointment(record) for record in df.to_dict(orient="records")] if isinstance(df, pd.DataFrame) else []
    return {"status": "success", "count": len(records), "appointments": records}

@router.get("/doctor/{doctor_email}")
def api_get_doctor_appointments(doctor_email: str):
    user_session = {"email": doctor_email, "role": "Doctor"}
    df = fetch_doctor_appointment_requests(user_session)
    records = [_frontend_appointment(record) for record in df.to_dict(orient="records")] if isinstance(df, pd.DataFrame) else []
    return {"status": "success", "count": len(records), "appointments": records}

@router.patch("/status")
def api_update_status(req: UpdateStatusRequest):
    user_session = {"email": req.doctor_email, "role": "Doctor"}
    _, msg = update_appointment_status(req.appointment_id, req.new_status, user_session)
    if "❌" in msg or "⚠️" in msg:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "success", "message": msg}
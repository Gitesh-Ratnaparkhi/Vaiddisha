# src/services/appointment_service.py
import pandas as pd
from src.repositories.appointment_repository import appointment_repository
from src.repositories.doctor_repository import doctor_repository

SLOT_OPTIONS = [
    "09:00 AM - 09:30 AM",
    "09:30 AM - 10:00 AM",
    "10:30 AM - 11:00 AM",
    "11:30 AM - 12:00 PM",
    "02:00 PM - 02:30 PM",
    "03:00 PM - 03:30 PM",
    "04:30 PM - 05:00 PM",
    "05:30 PM - 06:00 PM"
]

def get_registered_doctor_choices() -> list[str]:
    """Returns a list of formatted strings for doctor selection dropdown."""
    conn = doctor_repository.get_all_doctors()
    return [f"Dr. {r['name']} ({r['speciality']} - {r['hospital']}) | {r['email']}" for r in conn]

def book_new_appointment(patient_session: dict, doctor_selection: str, appointment_date: str, time_slot: str, reason: str) -> str:
    """Handles patient appointment booking request."""
    if not patient_session or not patient_session.get("logged_in"):
        return "⚠️ Please log in as a patient to book an appointment."
    
    if not doctor_selection or "|" not in doctor_selection:
        return "⚠️ Please select a valid doctor from the dropdown."
    
    if not appointment_date or not time_slot:
        return "⚠️ Please select both an appointment date and a time slot."

    patient_email = patient_session.get("email")
    if not patient_email:
        return "⚠️ Patient session is invalid or email is missing. Please log in again."
    patient_name = patient_session.get("name", "Patient")
    
    # Parse doctor name and email from formatted string
    doctor_email = doctor_selection.split("|")[-1].strip()
    doctor_name = doctor_selection.split("(")[0].strip()

    try:
        appointment_repository.create_appointment(
            patient_email=patient_email,
            patient_name=patient_name,
            doctor_email=doctor_email,
            doctor_name=doctor_name,
            appointment_date=str(appointment_date),
            time_slot=time_slot,
            reason=reason or "General Consultation"
        )
        return f"✅ **Appointment Requested!** Your request with **{doctor_name}** on **{appointment_date} ({time_slot})** is now pending doctor approval."
    except Exception as e:
        return f"❌ Failed to request appointment: {str(e)}"

def fetch_patient_appointments(patient_session: dict) -> pd.DataFrame:
    """Returns patient's scheduled appointments DataFrame."""
    if not patient_session:
        return pd.DataFrame(columns=["ID", "Doctor", "Date", "Slot", "Reason", "Status", "Requested At"])
    
    patient_email = patient_session.get("email")
    if not patient_email:
        return pd.DataFrame(columns=["ID", "Doctor", "Date", "Slot", "Reason", "Status", "Requested At"])
    
    data = appointment_repository.get_appointments_by_patient(patient_email)
    if not data:
        return pd.DataFrame(columns=["ID", "Doctor", "Date", "Slot", "Reason", "Status", "Requested At"])
    
    df = pd.DataFrame(data)
    df.rename(columns={
        "id": "ID",
        "doctor_name": "Doctor",
        "appointment_date": "Date",
        "time_slot": "Slot",
        "reason": "Reason",
        "status": "Status",
        "created_at": "Requested At"
    }, inplace=True)
    return df

def fetch_doctor_appointment_requests(doctor_session: dict) -> pd.DataFrame:
    """Returns doctor's appointment list DataFrame."""
    if not doctor_session:
        return pd.DataFrame(columns=["ID", "Patient Name", "Email", "Date", "Slot", "Reason", "Status"])
    
    doctor_email = doctor_session.get("email")
    if not doctor_email:
        return pd.DataFrame(columns=["ID", "Patient Name", "Email", "Date", "Slot", "Reason", "Status"])
    
    data = appointment_repository.get_appointments_by_doctor(doctor_email)
    if not data:
        return pd.DataFrame(columns=["ID", "Patient Name", "Email", "Date", "Slot", "Reason", "Status"])
    
    df = pd.DataFrame(data)
    df.rename(columns={
        "id": "ID",
        "patient_name": "Patient Name",
        "patient_email": "Email",
        "appointment_date": "Date",
        "time_slot": "Slot",
        "reason": "Reason",
        "status": "Status"
    }, inplace=True)
    return df

def update_appointment_status(appointment_id: int | str, new_status: str, doctor_session: dict) -> tuple[pd.DataFrame, str]:
    """Updates appointment status and returns refreshed table."""
    try:
        app_id = int(appointment_id)
        success = appointment_repository.update_appointment_status(app_id, new_status)
        msg = f"✅ Appointment #{app_id} marked as **{new_status}**." if success else f"⚠️ Appointment #{app_id} not found."
    except Exception as e:
        msg = f"❌ Error updating status: {str(e)}"
    
    refreshed_df = fetch_doctor_appointment_requests(doctor_session)
    return refreshed_df, msg
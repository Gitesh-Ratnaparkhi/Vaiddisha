# src/api/routes/doctor_routes.py
from fastapi import APIRouter, Query
from src.repositories.doctor_repository import doctor_repository
from src.services.appointment_service import get_registered_doctor_choices

router = APIRouter(prefix="/doctors", tags=["3. Doctors & Specialists"])

@router.get("/choices")
def api_get_doctor_choices():
    """Returns formatted doctor list for dropdown selectors."""
    choices = get_registered_doctor_choices()
    return {"status": "success", "count": len(choices), "doctors": choices}

@router.get("/search")
def api_search_doctors(
    speciality: str | None = Query(None, description="Doctor speciality e.g. Cardiologist"),
    city: str | None = Query(None, description="City e.g. Nagpur")
):
    """Searches registered doctors by city and/or speciality."""
    if city and speciality:
        docs = doctor_repository.get_doctors_by_city_and_speciality(city, speciality)
    elif speciality:
        docs = doctor_repository.get_doctors_by_speciality(speciality)
    else:
        docs = doctor_repository.get_all_doctors()
    
    return {"status": "success", "count": len(docs), "results": docs}
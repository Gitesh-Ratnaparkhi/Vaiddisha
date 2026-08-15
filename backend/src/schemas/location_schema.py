# src/schemas/location_schema.py
from typing import Optional
from pydantic import BaseModel

class LocationFilter(BaseModel):
    country: str
    state: Optional[str] = ""
    city: Optional[str] = ""

class DoctorSearchQuery(BaseModel):
    speciality: str
    country: Optional[str] = ""
    state: Optional[str] = ""
    city: Optional[str] = ""
# src/schemas/user_schema.py
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# --- BASE LOGIN SCHEMA ---
class UserLogin(BaseModel):
    email: str = Field(..., min_length=1, description="Account email address")
    password: str = Field(..., min_length=1, description="Account password")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower() if isinstance(v, str) else v


# --- PATIENT REGISTRATION SCHEMA ---
class PatientCreate(BaseModel):
    email: str = Field(..., min_length=1, description="Account email address")
    password: str = Field(..., min_length=9, description="Password must be > 8 characters")
    name: str = Field(..., min_length=2, description="Patient full name")
    gender: str = Field(default="Male")
    age: int = Field(default=25, ge=0, le=120)
    country: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    postal_code: Optional[str] = ""
    phone: Optional[str] = ""
    preferred_language: str = Field(default="English")
    existing_conditions: Optional[str] = ""
    previous_surgeries: Optional[str] = ""
    allergies: Optional[str] = ""

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower() if isinstance(v, str) else v

    @field_validator("password")
    @classmethod
    def check_password_length(cls, v: str) -> str:
        if len(v.strip()) <= 8:
            raise ValueError("Password must be more than 8 characters long.")
        return v.strip()


# --- DOCTOR REGISTRATION SCHEMA ---
class DoctorCreate(BaseModel):
    email: str = Field(..., min_length=1, description="Account email address")
    password: str = Field(..., min_length=9, description="Password must be > 8 characters")
    name: str = Field(..., min_length=2, description="Doctor full name")
    speciality: str = Field(..., min_length=2, description="Medical specialty")
    qualification: Optional[str] = ""
    experience: Optional[str] = ""
    hospital: Optional[str] = ""
    country: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    postal_code: Optional[str] = ""
    phone: Optional[str] = ""
    fee: Optional[str] = ""
    description: Optional[str] = Field("", description="Professional bio or summary (max 500 words)")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower() if isinstance(v, str) else v

    @field_validator("password")
    @classmethod
    def check_password_length(cls, v: str) -> str:
        if len(v.strip()) <= 8:
            raise ValueError("Password must be more than 8 characters long.")
        return v.strip()

    @field_validator("description")
    @classmethod
    def limit_description_words(cls, v: str) -> str:
        if v and len(v.strip().split()) > 500:
            raise ValueError("Description must not exceed 500 words.")
        return v.strip() if isinstance(v, str) else ""


# --- ACTIVE USER SESSION STATE SCHEMA ---
class UserSession(BaseModel):
    logged_in: bool = False
    email: str = ""
    role: str = ""
    name: str = ""
    terms_accepted: bool = False
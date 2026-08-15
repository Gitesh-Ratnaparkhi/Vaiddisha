# src/schemas/consultation_schema.py
from typing import Optional, List
from pydantic import BaseModel, Field

# --- SUSPECTED CONDITION ITEM ---
class ConditionPrediction(BaseModel):
    name: str
    probability: Optional[str] = ""
    explanation: Optional[str] = ""

# --- LLM AI DIAGNOSTIC RESPONSE MODEL ---
class DiagnosticOutput(BaseModel):
    summary: str = Field(default="No summary provided.")
    urgency_level: str = Field(default="Medium")  # Low, Medium, High, Emergency
    recommended_specialty: str = Field(default="General Physician")
    emergency_warning: Optional[str] = ""
    possible_conditions: List[ConditionPrediction] = Field(default_factory=list)

# --- CONSULTATION RECORD FOR DATABASE PERSISTENCE ---
class ConsultationCreate(BaseModel):
    patient_email: str
    patient_name: str
    symptoms: str
    summary: str
    urgency_level: str
    recommended_specialty: str
    status: str = Field(default="Pending")
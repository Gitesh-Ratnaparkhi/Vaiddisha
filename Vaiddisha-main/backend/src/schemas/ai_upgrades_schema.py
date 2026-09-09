# src/schemas/ai_upgrades_schema.py
from typing import Optional, List
from pydantic import BaseModel, Field

# --- 1. DYNAMIC TRIAGE SCHEMAS ---
class TriageQuestion(BaseModel):
    id: str
    question: str
    options: Optional[List[str]] = Field(default_factory=list)

class TriageState(BaseModel):
    initial_symptoms: str
    followup_questions: List[TriageQuestion] = Field(default_factory=list)
    patient_answers: dict = Field(default_factory=dict)
    is_complete: bool = False

# --- 2. MULTIMODAL OCR / VISION SCHEMAS ---
class MultimodalInput(BaseModel):
    image_path: Optional[str] = None
    pdf_document_path: Optional[str] = None
    extracted_text: Optional[str] = ""
    visual_description: Optional[str] = ""

# --- 3. ALLERGY & SAFETY CHECK SCHEMAS ---
class SafetyWarning(BaseModel):
    category: str  # "ALLERGY_CONFLICT", "CONDITION_CONTRAINDICATION", "DRUG_INTERACTION"
    severity: str  # "CRITICAL", "HIGH", "MODERATE"
    message: str

class SafetyCheckResult(BaseModel):
    is_safe: bool = True
    warnings: List[SafetyWarning] = Field(default_factory=list)
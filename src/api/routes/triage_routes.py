# src/api/routes/triage_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.triage_service import generate_triage_questions
from src.services.disease_service import process_disease_prediction
from src.security import llm_rate_limiter

router = APIRouter(prefix="/triage", tags=["2. Diagnostic Triage & Disease Prediction"])

class TriageQuestionsRequest(BaseModel):
    symptoms: str

class DiagnosticPredictionRequest(BaseModel):
    symptoms: str
    triage_answers: str = ""
    patient_email: str | None = None
    target_language: str = "English"

@router.post("/questions")
def api_generate_questions(req: TriageQuestionsRequest):
    if not req.symptoms.strip():
        raise HTTPException(status_code=400, detail="Symptoms text cannot be empty.")
    
    triage_state = generate_triage_questions(req.symptoms)
    return {
        "status": "success",
        "symptoms": req.symptoms,
        "questions": [q.model_dump() for q in triage_state.followup_questions]
    }

@router.post("/predict")
def api_predict_diagnosis(req: DiagnosticPredictionRequest):
    rate_key = req.patient_email or "guest_user"
    if not llm_rate_limiter.is_allowed(rate_key):
        raise HTTPException(status_code=429, detail="AI Inference rate limit reached. Please wait a moment.")

    session = {"email": req.patient_email} if req.patient_email else None
    analysis_md, pdf_path = process_disease_prediction(
        symptoms=req.symptoms,
        user_session=session,
        triage_answers=req.triage_answers,
        target_language=req.target_language
    )
    return {
        "status": "success",
        "analysis_markdown": analysis_md,
        "pdf_download_path": pdf_path
    }
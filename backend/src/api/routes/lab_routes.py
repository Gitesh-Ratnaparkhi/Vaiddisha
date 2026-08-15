# src/api/routes/lab_routes.py
import os
import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.services.lab_analyzer_service import analyze_medical_document
from src.exceptions import VaiddishaException

router = APIRouter(prefix="/lab", tags=["5. Medical Document & Lab Vision OCR"])

@router.post("/analyze")
async def api_analyze_lab_report(
    file: UploadFile = File(...),
    notes: str = Form(""),
    language: str = Form("English")
):
    ext = os.path.splitext(file.filename or "")[-1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Upload JPG, PNG, or WEBP.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        result_markdown = analyze_medical_document(
            image_path=temp_path,
            patient_notes=notes,
            target_language=language
        )
        return {
            "status": "success",
            "filename": file.filename,
            "analysis_markdown": result_markdown
        }
    except VaiddishaException as ve:
        raise HTTPException(status_code=ve.status_code, detail=ve.user_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
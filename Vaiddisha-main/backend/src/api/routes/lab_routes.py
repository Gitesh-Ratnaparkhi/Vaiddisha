# src/api/routes/lab_routes.py
import os
import shutil
import tempfile
import pymupdf
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
    if ext not in [".jpg", ".jpeg", ".png", ".webp", ".pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Upload a JPG, PNG, WEBP image, or PDF.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
    analysis_path = temp_path

    try:
        if ext == ".pdf":
            # The vision API accepts images, so rasterize the first report page.
            with pymupdf.open(temp_path) as document:
                if document.page_count == 0:
                    raise HTTPException(status_code=400, detail="The uploaded PDF has no pages.")
                page = document.load_page(0)
                pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
                rendered_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                rendered_file.close()
                pixmap.save(rendered_file.name)
                analysis_path = rendered_file.name

        result_markdown = analyze_medical_document(
            image_path=analysis_path,
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
        if analysis_path != temp_path and os.path.exists(analysis_path):
            os.remove(analysis_path)
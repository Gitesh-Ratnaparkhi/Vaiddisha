# src/services/lab_analyzer_service.py
import base64
from io import BytesIO
import os
from dotenv import load_dotenv
from groq import Groq
from PIL import Image, ImageEnhance, ImageFilter
from src.exceptions import (
    InvalidDocumentFormatError,
    LLMInferenceError,
    VisionOCRError,
)

load_dotenv()

VISION_SYSTEM_PROMPT = """You are Vaiddisha AI's Senior Clinical Laboratory & Diagnostic Expert.
Your task is to analyze patient medical lab test documents, blood test panels, imaging summaries, or pathology reports with high accuracy.

INSTRUCTIONS:
1. Use only text, numbers, units, ranges, and labels that are visibly present in the attached report.
2. Never invent, estimate, infer, or fill in a missing test, result, range, unit, patient detail, diagnosis, or recommendation.
3. If the image is blank, blurry, cropped, unreadable, or contains no lab results, say so clearly and do not create a sample result.
4. Extract the patient's Observed Value, the Reference Normal Range, and the Unit of Measurement only when they are visible.
5. Use standard medical spellings for clearly readable test names (for example, "Hemoglobin" rather than a phonetic guess), but never change a visible number, unit, or range.
6. Classify each visible metric into:
   - 🟢 NORMAL
   - 🟡 BORDERLINE / SLIGHTLY ELEVATED / SLIGHTLY LOW
   - 🔴 HIGH / ABNORMAL / CRITICAL
7. Keep clinical observations separate from report facts. Do not claim that a condition is present solely because a test could be related to it.
8. Format your output strictly in concise rich Markdown with these sections:
    - ### Quick read (1-2 short sentences summarizing the report)
    - ### Results to notice (a table with at most 8 visible tests; include Test, Result, Reference Range, and Status)
    - ### What to do next (at most 3 short bullets; mention a clinician or follow-up test only when supported by the findings)
    - ### Safety note (one short disclaimer sentence)
9. Keep the complete response under 450 words. Do not repeat normal results in the findings. Use plain patient-friendly language and short sentences.
10. Ensure the entire response is translated into the requested target language.
"""


def encode_image_to_base64(image_path: str) -> str:
    """Enhances and encodes a report image for more reliable text recognition."""
    try:
        with Image.open(image_path) as source_image:
            image = source_image.convert("RGB")
            width, height = image.size
            if max(width, height) < 1800:
                scale = min(2.0, 1800 / max(width, height))
                image = image.resize((int(width * scale), int(height * scale)), Image.Resampling.LANCZOS)
            image = ImageEnhance.Contrast(image).enhance(1.15)
            image = image.filter(ImageFilter.SHARPEN)
            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=95, optimize=True)
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        raise VisionOCRError(f"Failed to read image file: {str(e)}")


def analyze_medical_document(
    image_path: str,
    patient_notes: str = "",
    target_language: str = "English",
) -> str:
    """Analyzes medical lab document image using Groq Vision model."""
    if not image_path:
        return "⚠️ Please upload a medical lab report or document image first."

    # Validate file format
    ext = os.path.splitext(image_path)[-1].lower().replace(".", "")
    if ext not in ["png", "jpeg", "jpg", "webp"]:
        raise InvalidDocumentFormatError(extension=ext)

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise LLMInferenceError(
            "GROQ_API_KEY is not configured in environment variables."
        )

    try:
        client = Groq(api_key=api_key)
        base64_image = encode_image_to_base64(image_path)
        # The preprocessing pipeline normalizes every source image to JPEG.
        mime_type = "image/jpeg"

        user_content = [
            {
                "type": "text",
                "text": (
                    f"TARGET OUTPUT LANGUAGE: {target_language}\n"
                    f"ADDITIONAL PATIENT CONTEXT/NOTES: {patient_notes.strip() if patient_notes else 'None provided'}\n\n"
                    "Please examine this attached medical report image thoroughly, "
                    "extract only the information that is visibly present, and provide a cautious clinical interpretation. "
                    "Do not add any information that is not supported by the report."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
            },
        ]

        # pyrefly: ignore [no-matching-overload]
        response = client.chat.completions.create(
            model=os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.6-27b"),
            messages=[
                {"role": "system", "content": VISION_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.1,
            max_tokens=600,
        )

        return response.choices[0].message.content or ""

    except (InvalidDocumentFormatError, LLMInferenceError, VisionOCRError):
        raise
    except Exception as e:
        raise VisionOCRError(details=str(e))
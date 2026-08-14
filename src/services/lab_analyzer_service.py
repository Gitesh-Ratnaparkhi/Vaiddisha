# src/services/lab_analyzer_service.py
import base64
import os
from dotenv import load_dotenv
from groq import Groq
from src.exceptions import (
    InvalidDocumentFormatError,
    LLMInferenceError,
    VisionOCRError,
)

load_dotenv()

VISION_SYSTEM_PROMPT = """You are Vaiddisha AI's Senior Clinical Laboratory & Diagnostic Expert.
Your task is to analyze patient medical lab test documents, blood test panels, imaging summaries, or pathology reports with high accuracy.

INSTRUCTIONS:
1. Extract the key test parameters (e.g., Hemoglobin, WBC, Fasting Glucose, Cholesterol, Platelets, Creatinine, etc.).
2. Extract the patient's Observed Value, the Reference Normal Range, and the Unit of Measurement.
3. Classify each metric into:
   - 🟢 NORMAL
   - 🟡 BORDERLINE / SLIGHTLY ELEVATED / SLIGHTLY LOW
   - 🔴 HIGH / ABNORMAL / CRITICAL
4. Format your output strictly in rich Markdown with the following sections:
   - ### 📋 Report Overview & Test Type
   - ### 📊 Extracted Lab Test Metrics (Table format with columns: Test Name, Result Value, Reference Range, Status)
   - ### 🔍 Key Clinical Findings & Flagged Abnormalities (Explain out-of-range parameters in simple patient terms)
   - ### 🩺 Recommended Next Steps & Specialist Consultation (Specialist type to visit, further tests)
   - ### ⚠️ Clinical Disclaimer
5. Ensure the entire response is translated into the requested target language.
"""


def encode_image_to_base64(image_path: str) -> str:
    """Encodes a local image file to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
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
        mime_type = f"image/{ext}" if ext != "jpg" else "image/jpeg"

        user_content = [
            {
                "type": "text",
                "text": (
                    f"TARGET OUTPUT LANGUAGE: {target_language}\n"
                    f"ADDITIONAL PATIENT CONTEXT/NOTES: {patient_notes.strip() if patient_notes else 'None provided'}\n\n"
                    "Please examine this attached medical report image thoroughly, "
                    "extract all parameters, and provide your clinical interpretation."
                ),
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
            },
        ]

        # pyrefly: ignore [no-matching-overload]
        response = client.chat.completions.create(
            model=os.getenv("GROQ_VISION_MODEL", "llama-3.2-11b-vision-preview"),
            messages=[
                {"role": "system", "content": VISION_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content

    except (InvalidDocumentFormatError, LLMInferenceError, VisionOCRError):
        raise
    except Exception as e:
        raise VisionOCRError(details=str(e))
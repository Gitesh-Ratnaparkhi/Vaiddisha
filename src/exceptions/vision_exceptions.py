# src/exceptions/vision_exceptions.py
from src.exceptions.base import VaiddishaException

class InvalidDocumentFormatError(VaiddishaException):
    """Raised when an uploaded lab report has an unsupported file format."""
    def __init__(self, extension: str):
        super().__init__(
            message=f"Unsupported document format: '{extension}'",
            user_message="⚠️ Unsupported file format. Please upload a clear image (JPG, PNG, WEBP).",
            status_code=400
        )

class VisionOCRError(VaiddishaException):
    """Raised when the vision model fails to extract metrics from the image."""
    def __init__(self, details: str = ""):
        super().__init__(
            message=f"Vision OCR model processing failure: {details}",
            user_message="⚠️ Could not extract lab metrics. Please ensure the document is clear, well-lit, and legible.",
            status_code=502
        )
from typing import Optional
from src.schemas import MultimodalInput

def process_multimodal_attachments(image_path: Optional[str] = None, pdf_path: Optional[str] = None) -> MultimodalInput:
    """Processes image or PDF files to extract text or description."""
    return MultimodalInput(
        image_path=image_path,
        pdf_document_path=pdf_path,
        extracted_text="",
        visual_description=""
    )

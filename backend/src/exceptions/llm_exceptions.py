# src/exceptions/llm_exceptions.py
from src.exceptions.base import VaiddishaException

class LLMInferenceError(VaiddishaException):
    """Raised when the Groq LLM API fails, times out, or runs out of credits."""
    def __init__(self, original_error: str = ""):
        super().__init__(
            message=f"LLM inference error: {original_error}",
            user_message="⚠️ AI Diagnostic Engine is temporarily unavailable. Please check your internet connection or API key.",
            status_code=503
        )

class LLMResponseParsingError(VaiddishaException):
    """Raised when the LLM returns invalid or unparseable JSON/Markdown format."""
    def __init__(self, raw_output: str = ""):
        super().__init__(
            message=f"Failed to parse LLM structured output. Raw response: {raw_output[:100]}...",
            user_message="⚠️ Could not process the diagnostic response format. Please try rephrasing your symptoms.",
            status_code=422
        )
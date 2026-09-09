# src/exceptions/base.py

class VaiddishaException(Exception):
    """Base exception class for all custom errors in Vaiddisha AI."""
    
    def __init__(self, message: str = "An unexpected error occurred.", user_message: str | None = None, status_code: int = 500):
        super().__init__(message)
        self.message = message
        # Friendly user-facing string (safe to display on the Gradio UI)
        self.user_message = user_message or message
        self.status_code = status_code

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.status_code}): {self.message}"
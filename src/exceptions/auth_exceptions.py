# src/exceptions/auth_exceptions.py
from src.exceptions.base import VaiddishaException

class AuthenticationError(VaiddishaException):
    """Raised when user login or credential validation fails."""
    def __init__(self, message: str = "Invalid credentials provided."):
        super().__init__(
            message=message,
            user_message="⚠️ Incorrect email or password. Please verify and try again.",
            status_code=401
        )

class UserAlreadyExistsError(VaiddishaException):
    """Raised during registration when an email is already taken."""
    def __init__(self, email: str):
        super().__init__(
            message=f"Registration failed: User with email '{email}' already exists.",
            user_message=f"⚠️ An account with '{email}' already exists. Please sign in instead.",
            status_code=409
        )

class TermsNotAcceptedError(VaiddishaException):
    """Raised when a user attempts actions without accepting medical terms."""
    def __init__(self):
        super().__init__(
            message="User has not accepted terms and clinical disclaimer.",
            user_message="⚠️ You must review and accept the Clinical Terms & Disclaimer to proceed.",
            status_code=403
        )
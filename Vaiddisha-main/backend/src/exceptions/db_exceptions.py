# src/exceptions/db_exceptions.py
from src.exceptions.base import VaiddishaException

class DatabaseConnectionError(VaiddishaException):
    """Raised when the SQLite connection cannot be established or is locked."""
    def __init__(self, error: str = ""):
        super().__init__(
            message=f"Database connection failure: {error}",
            user_message="❌ Internal Database Error. Please contact support if this persists.",
            status_code=500
        )

class RecordNotFoundError(VaiddishaException):
    """Raised when querying an appointment, user, or consultation that does not exist."""
    def __init__(self, entity: str, identifier: str | int):
        super().__init__(
            message=f"{entity} with identifier '{identifier}' was not found.",
            user_message=f"⚠️ {entity} #{identifier} could not be found.",
            status_code=404
        )
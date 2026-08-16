# src/repositories/user_repository.py
from typing import Any
from src.repositories.database import get_connection

class UserRepository:

    @staticmethod
    def get_user_by_email(email: str):
        """
        Fetches base authentication credentials along with terms_accepted status.
        """
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()
        
        cursor.execute(
            "SELECT email, password_hash, role, terms_accepted FROM users WHERE email = %s", 
            (clean_email,)
        )
        row: Any = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def accept_terms(email: str) -> bool:
        """Updates the user's terms_accepted flag to 1 (True)."""
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()
        
        cursor.execute("UPDATE users SET terms_accepted = TRUE WHERE email = %s", (clean_email,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0

    @staticmethod
    def exists(email: str) -> bool:
        """Checks if a user with the given email already exists."""
        row = UserRepository.get_user_by_email(email)
        return row is not None

    @staticmethod
    def delete_user_by_email(email: str) -> bool:
        """Deletes a user account by email (cascades to patient/doctor profiles)."""
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()
        
        cursor.execute("DELETE FROM users WHERE email = %s", (clean_email,))
        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()
        return rows_affected > 0

# Single repository instance export
user_repository = UserRepository()
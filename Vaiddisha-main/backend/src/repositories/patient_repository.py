# src/repositories/patient_repository.py
from typing import Any
from src.repositories.database import get_connection

class PatientRepository:
    
    @staticmethod
    def create_patient_account(
        email: str, 
        hashed_password: str, 
        name: str, 
        gender: str, 
<<<<<<< HEAD
        age: int, 
=======
        birth_year: int | None,
>>>>>>> 57e9732 (Final commit after PP2)
        country: str,
        state: str,
        city: str,
        postal_code: str,
        phone: str, 
        language: str, 
        conditions: str, 
        surgeries: str, 
        allergies: str
    ):
        """Creates a patient user in 'users' and links their profile in 'patients' using email."""
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()
        
        try:
            # 1. Insert into users table
            cursor.execute(
                "INSERT INTO users (email, password_hash, role) VALUES (%s, %s, %s)", 
                (clean_email, hashed_password, "Patient")
            )

            # 2. Insert into patients table using email
            cursor.execute("""
                INSERT INTO patients (
<<<<<<< HEAD
                    email, name, gender, age, country, state, city, postal_code, 
                    phone, language, conditions, surgeries, allergies
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (clean_email, name, gender, age, country, state, city, postal_code, phone, language, conditions, surgeries, allergies))
=======
                    email, name, gender, birth_year, country, state, city, postal_code,
                    phone, language, conditions, surgeries, allergies
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (clean_email, name, gender, birth_year, country, state, city, postal_code, phone, language, conditions, surgeries, allergies))
>>>>>>> 57e9732 (Final commit after PP2)

            conn.commit()
            return clean_email
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_patient_by_email(email: str):
        """Fetches full patient profile using their email."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE email = %s", (email.strip().lower(),))
        row: Any = cursor.fetchone()
        conn.close()
        return row

patient_repository = PatientRepository()
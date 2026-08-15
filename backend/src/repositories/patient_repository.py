# src/repositories/patient_repository.py
from src.repositories.database import get_connection

class PatientRepository:
    
    @staticmethod
    def create_patient_account(
        email: str, 
        hashed_password: str, 
        name: str, 
        gender: str, 
        age: int, 
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
                "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)", 
                (clean_email, hashed_password, "Patient")
            )

            # 2. Insert into patients table using email
            cursor.execute("""
                INSERT INTO patients (
                    email, name, gender, age, country, state, city, postal_code, 
                    phone, preferred_language, existing_conditions, previous_surgeries, allergies
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (clean_email, name, gender, age, country, state, city, postal_code, phone, language, conditions, surgeries, allergies))

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
        cursor.execute("SELECT * FROM patients WHERE email = ?", (email.strip().lower(),))
        row = cursor.fetchone()
        conn.close()
        return row

patient_repository = PatientRepository()
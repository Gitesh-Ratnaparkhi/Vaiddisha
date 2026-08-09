# src/repositories/consultation_repository.py
from src.repositories.database import get_connection

class ConsultationRepository:

    @staticmethod
    def create_consultation(
        patient_email: str,
        patient_name: str,
        symptoms: str,
        summary: str,
        urgency_level: str,
        recommended_specialty: str
    ):
        """Creates a consultation record in the database."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO consultations (
                    patient_email, 
                    patient_name, 
                    symptoms, 
                    summary, 
                    urgency_level, 
                    recommended_specialty
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                patient_email.strip().lower(),
                patient_name.strip(),
                symptoms.strip(),
                summary.strip() if summary else "",
                urgency_level.strip() if urgency_level else "Medium",
                recommended_specialty.strip() if recommended_specialty else ""
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

consultation_repository = ConsultationRepository()

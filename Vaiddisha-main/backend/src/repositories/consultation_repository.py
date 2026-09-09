# src/repositories/consultation_repository.py
from src.repositories.database import get_connection

class ConsultationRepository:

    def create_consultation(
        self,
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
                ) VALUES (%s, %s, %s, %s, %s, %s)
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

    def get_consultations_by_patient(self, patient_email: str) -> list[dict]:
        """Fetches all past consultations recorded for a given patient email."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT id, symptoms, summary, urgency_level, recommended_specialty, created_at
                FROM consultations
                WHERE LOWER(patient_email) = %s
                ORDER BY id DESC
                """,
                (patient_email.strip().lower(),)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()


# Instantiate singleton for import across services
consultation_repository = ConsultationRepository()
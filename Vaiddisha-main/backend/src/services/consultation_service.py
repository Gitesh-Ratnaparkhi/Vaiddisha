# src/services/consultation_service.py
from typing import Any
from src.repositories.database import get_connection

def fetch_doctor_consultations():
    """Fetches all consultation records from PostgreSQL database to display on the doctor dashboard."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Querying columns corresponding to: ["ID", "Patient Name", "Symptoms", "Urgency", "Specialty", "Status", "Date"]
        # Since 'status' is not in PostgreSQL schema, we alias a default status 'Completed' dynamically.
        cursor.execute("SELECT id, patient_name, symptoms, urgency_level, recommended_specialty, 'Completed' AS status, created_at FROM consultations ORDER BY id DESC")
        rows: Any = cursor.fetchall()
        conn.close()
        
        result = []
        for row in rows:
            created_at_str = ""
            if row.get("created_at"):
                created_at_str = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            
            result.append([
                row.get("id"),
                row.get("patient_name"),
                row.get("symptoms"),
                row.get("urgency_level"),
                row.get("recommended_specialty"),
                row.get("status", "Completed"),
                created_at_str
            ])
        return result
    except Exception as e:
        print(f"Error fetching doctor consultations: {e}")
        return []

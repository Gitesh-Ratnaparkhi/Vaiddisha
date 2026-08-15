# src/services/consultation_service.py
import sqlite3

def fetch_doctor_consultations():
    """Fetches all consultation records from SQLite database to display on the doctor dashboard."""
    DB_PATH = "vaiddisha.db"
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Querying columns corresponding to: ["ID", "Patient Name", "Symptoms", "Urgency", "Specialty", "Status", "Date"]
        cursor.execute("SELECT id, patient_name, symptoms, urgency_level, recommended_specialty, status, created_at FROM consultations ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"Error fetching doctor consultations: {e}")
        return []

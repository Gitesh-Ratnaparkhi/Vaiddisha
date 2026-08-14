# src/repositories/appointment_repository.py
from src.repositories.database import get_connection

class AppointmentRepository:

    def create_appointment(
        self, 
        patient_email: str, 
        patient_name: str, 
        doctor_email: str, 
        doctor_name: str, 
        appointment_date: str, 
        time_slot: str, 
        reason: str
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO appointments (
                    patient_email, patient_name, doctor_email, 
                    doctor_name, appointment_date, time_slot, reason, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
            """, (
                patient_email.strip().lower(),
                patient_name.strip(),
                doctor_email.strip().lower(),
                doctor_name.strip(),
                appointment_date.strip(),
                time_slot.strip(),
                reason.strip()
            ))
            conn.commit()
            last_id = cursor.lastrowid
            if last_id is None:
                raise ValueError("Failed to create appointment: lastrowid is None")
            return last_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_appointments_by_patient(self, patient_email: str) -> list[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, doctor_name, appointment_date, time_slot, reason, status, created_at
                FROM appointments
                WHERE LOWER(patient_email) = ?
                ORDER BY id DESC
            """, (patient_email.strip().lower(),))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_appointments_by_doctor(self, doctor_email: str) -> list[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, patient_name, patient_email, appointment_date, time_slot, reason, status, created_at
                FROM appointments
                WHERE LOWER(doctor_email) = ?
                ORDER BY id DESC
            """, (doctor_email.strip().lower(),))
            rows = cursor.fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def update_appointment_status(self, appointment_id: int, new_status: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE appointments
                SET status = ?
                WHERE id = ?
            """, (new_status, appointment_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

appointment_repository = AppointmentRepository()
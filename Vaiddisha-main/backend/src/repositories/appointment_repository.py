# src/repositories/appointment_repository.py
from typing import Any
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
                    patient_email, doctor_email, date, slot, reason, status
                ) VALUES (%s, %s, %s, %s, %s, 'Pending')
                RETURNING id
            """, (
                patient_email.strip().lower(),
                doctor_email.strip().lower(),
                appointment_date.strip(),
                time_slot.strip(),
                reason.strip()
            ))
            conn.commit()
            row: Any = cursor.fetchone()
            if not row or 'id' not in row:
                raise ValueError("Failed to create appointment: no id returned")
            return row['id']
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
                SELECT a.id, d.name AS doctor_name, a.date AS appointment_date, a.slot AS time_slot, a.reason, a.status, a.created_at
                FROM appointments a
                JOIN doctors d ON a.doctor_email = d.email
                WHERE LOWER(a.patient_email) = %s
                ORDER BY a.id DESC
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
                SELECT a.id, p.name AS patient_name, a.patient_email, a.date AS appointment_date, a.slot AS time_slot, a.reason, a.status, a.created_at
                FROM appointments a
                JOIN patients p ON a.patient_email = p.email
                WHERE LOWER(a.doctor_email) = %s
                ORDER BY a.id DESC
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
                SET status = %s
                WHERE id = %s
            """, (new_status, appointment_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

appointment_repository = AppointmentRepository()
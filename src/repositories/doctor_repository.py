# src/repositories/doctor_repository.py
from src.repositories.database import get_connection

class DoctorRepository:

    @staticmethod
    def create_doctor_account(
        email: str,
        password_hash: bytes,
        name: str,
        speciality: str,
        qualification: str,
        experience: str,
        hospital: str,
        country: str,
        state: str,
        city: str,
        postal_code: str,
        phone: str,
        fee: str,
        description: str
    ):
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()

        # Insert user login credentials
        cursor.execute(
            "INSERT INTO users (email, password_hash, role, terms_accepted) VALUES (?, ?, ?, 0)",
            (clean_email, password_hash, "Doctor")
        )

        # Insert doctor profile details
        cursor.execute("""
            INSERT INTO doctors (
                email, name, speciality, qualification, experience, hospital,
                country, state, city, postal_code, phone, fee, description
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            clean_email, name.strip(), speciality.strip(), qualification.strip(),
            experience.strip(), hospital.strip(), country.strip(), state.strip(),
            city.strip(), postal_code.strip(), phone.strip(), fee.strip(), description.strip()
        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_doctor_by_email(email: str):
        conn = get_connection()
        cursor = conn.cursor()
        clean_email = email.strip().lower()

        cursor.execute("SELECT * FROM doctors WHERE email = ?", (clean_email,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def get_doctors_by_speciality(speciality: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE LOWER(speciality) = ?", (speciality.strip().lower(),))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_doctors_by_city_and_speciality(city: str, speciality: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM doctors WHERE LOWER(city) = ? AND LOWER(speciality) = ?",
            (city.strip().lower(), speciality.strip().lower())
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

doctor_repository = DoctorRepository()
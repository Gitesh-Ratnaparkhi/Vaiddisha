# src/services/auth_service.py
import bcrypt
from src.repositories.user_repository import user_repository
from src.repositories.patient_repository import patient_repository
from src.repositories.doctor_repository import doctor_repository

def register_patient(
    email: str, 
    password: str, 
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
) -> str:
    clean_email = email.strip().lower()

    if not clean_email or not password.strip() or not name.strip():
        return "⚠️ Email, Password, and Full Name are required."

    if len(password.strip()) <= 8:
        return "⚠️ Password must be more than 8 characters long."

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        patient_repository.create_patient_account(
            clean_email, hashed, name, gender, age, 
            country, state, city, postal_code, 
            phone, language, conditions, surgeries, allergies
        )
        return f"🎉 Account created successfully for **{name}**! You can now log in with {clean_email}."

    except Exception as e:
        if "UNIQUE constraint failed" in str(e) or "PRIMARY KEY" in str(e):
            return "❌ This email address is already registered."
        return f"❌ Registration failed: {str(e)}"


def register_doctor(
    email: str, 
    password: str, 
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
    description: str = ""
) -> str:
    """Registers a new doctor profile with professional description."""
    clean_email = email.strip().lower()

    if not clean_email or not password.strip() or not name.strip() or not speciality.strip():
        return "⚠️ Email, Password, Name, and Speciality are required."

    if len(password.strip()) <= 8:
        return "⚠️ Password must be more than 8 characters long."

    # Validate word limit (max 500 words)
    words = description.strip().split()
    if len(words) > 500:
        return f"⚠️ Doctor description exceeds 500 words ({len(words)} words entered). Please shorten it."

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        doctor_repository.create_doctor_account(
            clean_email, hashed, name, speciality, qualification, 
            experience, hospital, country, state, city, postal_code, phone, fee, description
        )
        return f"🎉 Doctor account registered for **Dr. {name}**! You can now log in with {clean_email}."

    except Exception as e:
        if "UNIQUE constraint failed" in str(e) or "PRIMARY KEY" in str(e):
            return "❌ This email address is already registered."
        return f"❌ Registration failed: {str(e)}"


def login_user(email: str, password: str) -> tuple[bool, str, dict]:
    clean_email = email.strip().lower()
    if not clean_email or not password.strip():
        return False, "⚠️ Please enter email and password.", {}

    try:
        user = user_repository.get_user_by_email(clean_email)
        if not user:
            return False, "❌ Invalid email or password.", {}

        stored_hash = user["password_hash"]
        role = user["role"]
        terms_accepted = bool(user["terms_accepted"])

        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            if role == "Patient":
                profile = patient_repository.get_patient_by_email(clean_email)
                name = profile["name"] if profile else "Patient"
            else:
                profile = doctor_repository.get_doctor_by_email(clean_email)
                name = profile["name"] if profile else "Doctor"

            user_session = {
                "logged_in": True,
                "email": clean_email,
                "role": role,
                "name": name,
                "terms_accepted": terms_accepted
            }
            return True, f"✅ Welcome back, {name}!", user_session
        else:
            return False, "❌ Invalid email or password.", {}

    except Exception as e:
        return False, f"❌ Authentication error: {str(e)}", {}


def confirm_terms_acceptance(email: str) -> tuple[bool, str]:
    success = user_repository.accept_terms(email)
    if success:
        return True, "✅ Terms and Conditions accepted."
    return False, "❌ Failed to update Terms acceptance status."
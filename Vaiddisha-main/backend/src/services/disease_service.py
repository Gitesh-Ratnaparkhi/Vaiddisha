# src/services/disease_service.py
import re
from datetime import datetime

from src.llm.llm_service import llm_service
from src.llm.rag_service import rag_service
from src.services.multimodal_service import process_multimodal_attachments
from src.services.safety_service import safety_service
from src.repositories.patient_repository import patient_repository
from src.repositories.doctor_repository import doctor_repository
from src.repositories.consultation_repository import consultation_repository
from src.utils.pdf_generator import generate_medical_report_pdf
from src.security import sanitize_text, redact_pii_for_llm, is_potential_prompt_injection


def _demographics_from_symptoms(symptoms: str) -> tuple[int | None, str | None]:
    """Use only explicit age/gender phrases when profile values are unavailable."""
    age_match = re.search(r"\b(\d{1,3})\s*(?:years?|yrs?)[ -]*old\b", symptoms, re.IGNORECASE)
    gender_match = re.search(r"\b(female|woman| girl|male|man| boy)\b", symptoms, re.IGNORECASE)
    age = int(age_match.group(1)) if age_match else None
    gender = None
    if gender_match:
        gender = "Female" if gender_match.group(1).strip().lower() in {"female", "woman", "girl"} else "Male"
    return age, gender


def _current_age(patient_profile: dict | None) -> int | None:
    if not patient_profile:
        return None
    birth_year = patient_profile.get("birth_year")
    if birth_year:
        return datetime.now().year - int(birth_year)
    stored_age = patient_profile.get("age")
    return stored_age if stored_age not in (None, "", 0) else None


def _relevant_fallback_specialties(symptoms: str, recommended_specialty: str) -> list[str]:
    text = f"{symptoms} {recommended_specialty}".lower()
    specialty_map = [
        (("chest pain", "chest tightness", "heart", "palpitation", "shortness of breath", "breathlessness"), "Cardiologist"),
        (("skin", "rash", "acne", "itching"), "Dermatologist"),
        (("pregnan", "period", "menstrual", "ovary", "uterus"), "Gynaecologist"),
        (("sugar", "diabet", "glucose"), "Diabetologist"),
        (("cancer", "tumor", "oncolog"), "Oncologist"),
        (("tooth", "teeth", "gum", "dental"), "Dentist"),
    ]
    return [specialty for keywords, specialty in specialty_map if any(keyword in text for keyword in keywords)]

def process_disease_prediction(
    symptoms: str, 
    user_session: dict | None = None, 
    image_file: str | None = None, 
    pdf_file: str | None = None,
    triage_answers: str = "",
    target_language: str = "English",
    include_doctors: bool = False,
) -> tuple:
    """
    Master diagnostic pipeline returning (formatted_markdown, pdf_report_path)
    with integrated input sanitization, prompt injection defense, and PII redaction.
    """
    if not symptoms or not symptoms.strip():
        return "⚠️ Please enter or record your symptoms before running analysis.", None

    try:
        session = user_session or {}
        email = session.get("email", "")
        patient_profile = None

        if email:
            patient_row = patient_repository.get_patient_by_email(email)
            if patient_row:
                patient_profile = dict(patient_row)

        # 🔒 Security Step 1: Sanitize text input
        clean_symptoms = sanitize_text(symptoms)

        # 🔒 Security Step 2: Check for prompt injection attempts
        if is_potential_prompt_injection(clean_symptoms):
            clean_symptoms = "User entered an invalid or restricted symptom description."

        # 🔒 Security Step 3: Strip accidental PII before sending to external LLM API
        safe_symptoms = redact_pii_for_llm(clean_symptoms)

        # 1. Process Multimodal Attachments
        mm_data = process_multimodal_attachments(image_path=image_file, pdf_path=pdf_file)
        combined_context_symptoms = safe_symptoms
        if mm_data.extracted_text:
            combined_context_symptoms += f"\n\n{sanitize_text(mm_data.extracted_text)}"
        if mm_data.visual_description:
            combined_context_symptoms += f"\n\n{sanitize_text(mm_data.visual_description)}"
        if triage_answers:
            safe_triage = redact_pii_for_llm(sanitize_text(triage_answers))
            combined_context_symptoms += f"\n\n📋 [Follow-Up Context]: {safe_triage}"

        # 2. Retrieve RAG Clinical Guidelines
        guidelines = rag_service.retrieve_guidelines(combined_context_symptoms)
        if guidelines:
            guidelines_text = "\n".join(guidelines)
            combined_context_symptoms += f"\n\n{guidelines_text}"

        # 3. LLM Diagnostic Inference (using PII-redacted, sanitized payload)
        diagnosis = llm_service.analyze_symptoms(
            combined_context_symptoms, 
            patient_profile, 
            target_language=target_language
        )

        # 4. Safety & Allergy Audits
        safety_res = safety_service.check_patient_safety(diagnosis, patient_profile)

        # 5. Doctor Recommendations
        city = (patient_profile.get("city") if patient_profile else "") or "Nagpur"
        specialty = diagnosis.recommended_specialty

        doctors = []
        if city and specialty:
            doctors = doctor_repository.get_doctors_by_city_and_speciality(city, specialty)
        elif specialty:
            doctors = doctor_repository.get_doctors_by_speciality(specialty)

        if not doctors and city:
            for fallback_specialty in _relevant_fallback_specialties(symptoms, specialty):
                doctors.extend(doctor_repository.get_doctors_by_city_and_speciality(city, fallback_specialty))
                if len(doctors) >= 3:
                    break
            doctors = doctors[:3]

        # 6. Record Consultation History
        patient_name = patient_profile.get("name", "Patient") if patient_profile else "Guest Patient"
        if email and patient_profile:
            consultation_repository.create_consultation(
                patient_email=email,
                patient_name=patient_name,
                symptoms=symptoms,
                summary=diagnosis.summary,
                urgency_level=diagnosis.urgency_level,
                recommended_specialty=diagnosis.recommended_specialty
            )

        # 7. Generate PDF Report
        extracted_age, extracted_gender = _demographics_from_symptoms(symptoms)
        report_age = _current_age(patient_profile) or extracted_age
        report_gender = patient_profile.get("gender") if patient_profile and patient_profile.get("gender") not in (None, "", "Unspecified") else extracted_gender
        pdf_path = generate_medical_report_pdf(
            patient_name=patient_name,
            email=email,
            symptoms=symptoms,
            diagnosis=diagnosis,
            doctors=doctors,
            safety_res=safety_res,
            age=report_age,
            gender=report_gender,
            target_language=target_language,
        )

        formatted_md = _format_ui_markdown(diagnosis, doctors, safety_res)
        if include_doctors:
            return formatted_md, pdf_path, doctors
        return formatted_md, pdf_path

    except Exception as e:
        error_msg = f"❌ **Diagnostic Pipeline Error:** {str(e)}"
        if include_doctors:
            return error_msg, None, []
        return error_msg, None


def _format_ui_markdown(diagnosis, doctors, safety_res) -> str:
    urgency_badge = {
        "Low": "🟢 **Low Risk**",
        "Medium": "🟡 **Moderate Urgency**",
        "High": "🟠 **High Urgency**",
        "Emergency": "🔴 **EMERGENCY WARNING**"
    }.get(diagnosis.urgency_level, "🟡 **Moderate Urgency**")

    md = f"### {urgency_badge}\n\n"

    if not safety_res.is_safe:
        md += "### 🛡️ **PATIENT SAFETY WARNINGS:**\n"
        for w in safety_res.warnings:
            md += f"> ⚠️ **[{w.category}]** ({w.severity}): {w.message}\n"
        md += "\n---\n"

    if diagnosis.emergency_warning:
        md += f"> ⚠️ **ALERT:** {diagnosis.emergency_warning}\n\n"

    md += f"**Clinical Summary:** {diagnosis.summary}\n\n"
    md += f"**Recommended Specialist:** `{diagnosis.recommended_specialty}`\n\n"

    md += "#### 🔍 Suspected Conditions:\n"
    for cond in diagnosis.possible_conditions:
        md += f"- **{cond.name}** (Probability: *{cond.probability}*)\n  _{cond.explanation}_\n"

    md += "\n---\n#### 👨‍⚕️ Recommended Nearby Specialists:\n"
    if doctors:
        for doc in doctors[:3]:
            md += f"- **Dr. {doc['name']}** ({doc['speciality']}) — {doc['hospital']}, {doc['city']}\n"
            md += f"  - 🎓 {doc['qualification']} | 💼 Experience: {doc['experience']}\n"
            md += f"  - 📞 Contact: {doc['phone']} | Fee: {doc['fee']}\n"
    else:
        if diagnosis.urgency_level == "Emergency":
            md += "_No matching specialist is listed locally. Go to the nearest emergency department or call 112 immediately._\n"
        else:
            md += f"_No registered {diagnosis.recommended_specialty} doctors found in your city._\n"

    return md
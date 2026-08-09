# src/services/disease_service.py
from src.llm.llm_service import llm_service
from src.llm.rag_service import rag_service
from src.services.multimodal_service import process_multimodal_attachments
from src.services.safety_service import safety_service
from src.repositories.patient_repository import patient_repository
from src.repositories.doctor_repository import doctor_repository
from src.repositories.consultation_repository import consultation_repository
from src.utils.pdf_generator import generate_medical_report_pdf

def process_disease_prediction(
    symptoms: str, 
    user_session: dict | None = None, 
    image_file: str | None = None, 
    pdf_file: str | None = None,
    triage_answers: str = ""
) -> tuple[str, str | None]:
    """
    Master diagnostic pipeline returning (formatted_markdown, pdf_report_path).
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

        # 1. Process Multimodal Attachments
        mm_data = process_multimodal_attachments(image_path=image_file, pdf_path=pdf_file)
        combined_context_symptoms = symptoms.strip()
        if mm_data.extracted_text:
            combined_context_symptoms += f"\n\n{mm_data.extracted_text}"
        if mm_data.visual_description:
            combined_context_symptoms += f"\n\n{mm_data.visual_description}"
        if triage_answers:
            combined_context_symptoms += f"\n\n📋 [Follow-Up Context]: {triage_answers}"

        # 2. Retrieve RAG Clinical Guidelines
        guidelines = rag_service.retrieve_guidelines(combined_context_symptoms)
        if guidelines:
            guidelines_text = "\n".join(guidelines)
            combined_context_symptoms += f"\n\n{guidelines_text}"

        # 3. LLM Diagnostic Inference
        diagnosis = llm_service.analyze_symptoms(combined_context_symptoms, patient_profile)

        # 4. Safety & Allergy Audits
        safety_res = safety_service.check_patient_safety(diagnosis, patient_profile)

        # 5. Doctor Recommendations
        city = patient_profile.get("city", "") if patient_profile else ""
        specialty = diagnosis.recommended_specialty

        doctors = []
        if city and specialty:
            doctors = doctor_repository.get_doctors_by_city_and_speciality(city, specialty)
        elif specialty:
            doctors = doctor_repository.get_doctors_by_speciality(specialty)

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
        pdf_path = generate_medical_report_pdf(
            patient_name=patient_name,
            email=email,
            symptoms=symptoms,
            diagnosis=diagnosis,
            doctors=doctors,
            safety_res=safety_res
        )

        formatted_md = _format_ui_markdown(diagnosis, doctors, safety_res)
        return formatted_md, pdf_path

    except Exception as e:
        error_msg = f"❌ **Diagnostic Pipeline Error:** {str(e)}"
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
        md += f"_No registered {diagnosis.recommended_specialty} doctors found in your city. Consult a General Physician._\n"

    return md
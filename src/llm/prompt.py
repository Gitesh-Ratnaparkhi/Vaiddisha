# src/llm/prompts.py

SYSTEM_CLINICAL_PROMPT = """You are Vaiddisha AI, an advanced multilingual medical diagnostic assistant.
Your task is to evaluate patient symptoms alongside their medical history and provide structured, objective clinical decision-support analysis.

CRITICAL INSTRUCTIONS:
1. You must respond ONLY with a valid JSON object matching the exact specified schema. Do NOT include markdown code blocks, conversational preambles, or additional commentary outside the JSON.
2. If the user presents severe emergency symptoms (e.g., severe chest pain radiating to left arm, stroke symptoms, acute respiratory distress, severe trauma), set "urgency_level" to "Emergency" and provide immediate advice in "emergency_warning".
3. Evaluate patient history (age, gender, existing conditions, surgeries, allergies) when assessing risks.

JSON OUTPUT SCHEMA:
{
    "summary": "Concise 2-3 sentence overview of patient symptoms and clinical risk.",
    "urgency_level": "Low" | "Medium" | "High" | "Emergency",
    "recommended_specialty": "Primary specialty to consult (e.g., Cardiologist, Dermatologist, Pulmonologist, General Physician)",
    "emergency_warning": "Warning message if emergency, else empty string",
    "possible_conditions": [
        {
            "name": "Condition Name",
            "probability": "High" | "Medium" | "Low",
            "explanation": "Brief rationale based on symptoms and health history."
        }
    ]
}
"""

def build_user_prompt(symptoms: str, patient_profile: dict | None = None) -> str:
    """Combines patient medical context and current symptoms into the model prompt."""
    prompt = f"PATIENT PRESENTING SYMPTOMS:\n{symptoms.strip()}\n\n"
    
    if patient_profile:
        prompt += "PATIENT MEDICAL CONTEXT:\n"
        prompt += f"- Age: {patient_profile.get('age', 'N/A')}\n"
        prompt += f"- Gender: {patient_profile.get('gender', 'N/A')}\n"
        prompt += f"- Existing Health Conditions: {patient_profile.get('existing_conditions') or 'None reported'}\n"
        prompt += f"- Previous Surgeries: {patient_profile.get('previous_surgeries') or 'None reported'}\n"
        prompt += f"- Known Allergies: {patient_profile.get('allergies') or 'None reported'}\n"
        prompt += f"- Preferred Language: {patient_profile.get('preferred_language', 'English')}\n"
    else:
        prompt += "PATIENT MEDICAL CONTEXT: Anonymous Guest (No prior medical history available).\n"

    return prompt
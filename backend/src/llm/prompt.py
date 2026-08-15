# src/llm/prompts.py

SYSTEM_CLINICAL_PROMPT = """You are Vaiddisha AI, an advanced multilingual medical diagnostic assistant.
Your task is to evaluate patient symptoms alongside their medical history and provide structured, objective clinical decision-support analysis.

CRITICAL INSTRUCTIONS:
1. You must respond ONLY with a valid JSON object matching the exact specified schema. Do NOT include markdown code blocks, conversational preambles, or additional commentary outside the JSON.
2. Ensure ALL textual fields ("summary", "recommended_specialty", "emergency_warning", condition "name", and condition "explanation") are written in the requested Target Language specified in the prompt.
3. If the user presents severe emergency symptoms, set "urgency_level" to "Emergency" and provide immediate advice in "emergency_warning".

JSON OUTPUT SCHEMA:
{
    "summary": "Concise overview of patient symptoms and clinical risk in target language.",
    "urgency_level": "Low" | "Medium" | "High" | "Emergency",
    "recommended_specialty": "Primary specialty to consult in target language",
    "emergency_warning": "Warning message if emergency, else empty string",
    "possible_conditions": [
        {
            "name": "Condition Name in target language",
            "probability": "High" | "Medium" | "Low",
            "explanation": "Brief rationale in target language based on symptoms and health history."
        }
    ]
}
"""


def build_user_prompt(
    symptoms: str,
    patient_profile: dict | None = None,
    target_language: str = "English",
) -> str:
    """Combines medical context, symptoms, and target output language instruction into the prompt."""
    prompt = f"TARGET OUTPUT LANGUAGE: Respond entirely in {target_language}.\n\n"
    prompt += f"PATIENT PRESENTING SYMPTOMS:\n{symptoms.strip()}\n\n"

    if patient_profile:
        prompt += "PATIENT MEDICAL CONTEXT:\n"
        prompt += f"- Age: {patient_profile.get('age', 'N/A')}\n"
        prompt += f"- Gender: {patient_profile.get('gender', 'N/A')}\n"
        prompt += f"- Existing Health Conditions: {patient_profile.get('existing_conditions') or 'None reported'}\n"
        prompt += f"- Previous Surgeries: {patient_profile.get('previous_surgeries') or 'None reported'}\n"
        prompt += f"- Known Allergies: {patient_profile.get('allergies') or 'None reported'}\n"
    else:
        prompt += "PATIENT MEDICAL CONTEXT: Anonymous Guest (No prior medical history available).\n"

    return prompt
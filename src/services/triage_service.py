# src/services/triage_service.py
import json
from src.llm.llm_service import llm_service
from src.schemas import TriageQuestion, TriageState

TRIAGE_PROMPT_TEMPLATE = """You are a clinical triage assistant.
A patient presents with the following initial symptoms: "{symptoms}"

Generate 2 to 3 targeted, clinical clarifying follow-up questions to narrow down the diagnosis (e.g., onset duration, pain scale, fever degree, aggravating factors).

OUTPUT STRICTLY IN THIS JSON FORMAT:
{{
    "questions": [
        {{
            "id": "q1",
            "question": "How long have you been experiencing these symptoms?",
            "options": ["Less than 24 hours", "1-3 days", "More than a week"]
        }},
        {{
            "id": "q2",
            "question": "Is the pain sharp, dull, throbbing, or burning?",
            "options": ["Sharp", "Dull", "Throbbing", "Burning"]
        }}
    ]
}}
"""

def generate_triage_questions(symptoms: str) -> TriageState:
    """Analyzes initial symptoms and returns structured follow-up questions."""
    if not symptoms or len(symptoms.strip()) < 5:
        return TriageState(initial_symptoms=symptoms, is_complete=True)

    prompt = TRIAGE_PROMPT_TEMPLATE.format(symptoms=symptoms)
    try:
        # pyrefly: ignore [no-matching-overload]
        response = llm_service.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        if content is None:
            raise ValueError("No response content received from LLM.")
        data = json.loads(content)
        raw_qs = data.get("questions", [])
        
        questions = [
            TriageQuestion(
                id=q.get("id", f"q{idx}"),
                question=q.get("question", ""),
                options=q.get("options", [])
            )
            for idx, q in enumerate(raw_qs)
        ]
        return TriageState(initial_symptoms=symptoms, followup_questions=questions, is_complete=False)

    except Exception as e:
        print(f"[Triage Service Warning]: {e}")
        return TriageState(initial_symptoms=symptoms, is_complete=True)
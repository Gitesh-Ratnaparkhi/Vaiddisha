# src/llm/parser.py
import json
import re
from src.schemas import DiagnosticOutput, ConditionPrediction

def _get_fallback_output(error_msg: str) -> DiagnosticOutput:
    """Returns a fallback model structure in case parsing fails."""
    return DiagnosticOutput(
        summary=f"Fallback: {error_msg}",
        urgency_level="Medium",
        recommended_specialty="General Physician",
        emergency_warning="Could not parse diagnostic output correctly.",
        possible_conditions=[]
    )

def parse_llm_json_response(raw_response: str) -> DiagnosticOutput:
    """
    Cleans raw LLM text, strips markdown code blocks, and converts it into a DiagnosticOutput model.
    Falls back gracefully if the LLM output is malformed.
    """
    if not raw_response or not raw_response.strip():
        return _get_fallback_output("Empty response received from LLM model.")

    try:
        # Strip Markdown blocks (```json ... ``` or ``` ...)
        cleaned_text = re.sub(r"```json\s*", "", raw_response)
        cleaned_text = re.sub(r"```\s*", "", cleaned_text)
        cleaned_text = cleaned_text.strip()

        # Find the first occurrences of { and the last occurrence of } to extract JSON
        start_idx = cleaned_text.find('{')
        end_idx = cleaned_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            cleaned_text = cleaned_text[start_idx:end_idx+1]

        data = json.loads(cleaned_text)
        return DiagnosticOutput(**data)
    except Exception as e:
        return _get_fallback_output(f"Failed to parse LLM response: {str(e)}")
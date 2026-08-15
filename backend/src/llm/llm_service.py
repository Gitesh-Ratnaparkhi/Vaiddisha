# src/llm/llm_service.py
import os
from dotenv import load_dotenv
from groq import Groq
# pyrefly: ignore [missing-import]
from src.llm.prompt import SYSTEM_CLINICAL_PROMPT, build_user_prompt
from src.llm.parser import parse_llm_json_response
from src.schemas.consultation_schema import DiagnosticOutput

# Automatically load environment variables from .env file when imported
load_dotenv()

class LLMService:
    @property
    def client(self) -> Groq:
        """Exposes the dynamically configured Groq client instance."""
        return self._get_client()

    def _get_client(self) -> Groq:
        """Dynamically fetches the latest GROQ_API_KEY from environment variables."""
        api_key = os.getenv("GROQ_API_KEY", "").strip()

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing or empty in your environment (.env).")

        return Groq(api_key=api_key)

    def analyze_symptoms(
        self, 
        symptoms: str, 
        patient_profile: dict | None = None, 
        target_language: str = "English"
    ) -> DiagnosticOutput:
        """Calls Groq Llama 3.3 model and returns validated diagnostic response in target language."""
        try:
            client = self._get_client()
            model_name = os.getenv("GROK_MODEL", "llama-3.3-70b-versatile").strip()

            user_prompt = build_user_prompt(
                symptoms=symptoms, 
                patient_profile=patient_profile, 
                target_language=target_language
            )

            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_CLINICAL_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            raw_text = response.choices[0].message.content
            if raw_text is None:
                raise ValueError("LLM returned an empty response content.")

            return parse_llm_json_response(raw_text)

        except Exception as e:
            raise RuntimeError(f"Groq API Error: {str(e)}")

# Create a singleton instance for simple importing across services
llm_service = LLMService()
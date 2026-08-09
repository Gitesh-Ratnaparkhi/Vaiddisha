# src/llm/llm_service.py
from openai import OpenAI
import src.config.config as config
from src.llm.prompt import SYSTEM_CLINICAL_PROMPT, build_user_prompt
from src.llm.parser import parse_llm_json_response
from src.schemas import DiagnosticOutput

class LLMService:
    @property
    def client(self) -> OpenAI:
        """
        Exposes the dynamically configured client instance to ensure fresh credentials are used.
        """
        return self._get_client()

    def _get_client(self) -> OpenAI:
        """
        Dynamically fetches the latest API key from config on every call
        to prevent caching stale or invalid credentials.
        """
        # Always reload config parameters dynamically
        api_key = config.XAI_API_KEY
        base_url = config.XAI_BASE_URL

        if not api_key:
            raise ValueError("GROQ_API_KEY is missing or empty in your environment (.env).")

        return OpenAI(
            api_key=api_key,
            base_url=base_url
        )

    def analyze_symptoms(self, symptoms_text: str, patient_profile: dict | None = None) -> DiagnosticOutput:
        """
        Sends patient symptom description to Groq Cloud (Llama 3.3) 
        and returns structured diagnostic analysis as a DiagnosticOutput object.
        """
        try:
            # Get fresh client instance
            client = self._get_client()

            user_content = build_user_prompt(symptoms_text, patient_profile)

            response = client.chat.completions.create(
                model=config.GROK_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_CLINICAL_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.2,  # Low randomness for consistent clinical evaluations
                response_format={"type": "json_object"}  # Guarantees valid JSON output
            )

            raw_content = response.choices[0].message.content
            if raw_content is None:
                raise ValueError("LLM returned an empty response content.")
            
            # Clean and parse JSON output
            parsed_json = parse_llm_json_response(raw_content)
            return parsed_json

        except Exception as e:
            raise RuntimeError(f"LLMService Execution Error: {str(e)}")

# Create a singleton instance for simple importing across services
llm_service = LLMService()
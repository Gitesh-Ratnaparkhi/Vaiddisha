import os
from dotenv import load_dotenv

# Force reload environment variables from .env to prevent cached invalid keys
load_dotenv(override=True)

# Groq Cloud API Credentials & Base URL
XAI_API_KEY = os.getenv("GROQ_API_KEY")
XAI_BASE_URL = "https://api.groq.com/openai/v1"

# Default Model Selection (Groq Cloud)
GROK_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Clinical Assistant Prompt Template
GROK_SYSTEM_PROMPT = """
You are a clinical decision-support AI assistant.
Analyze the user's description of symptoms.

Respond ONLY in valid, raw JSON format with no additional surrounding conversational text.

Required JSON Structure:
{
    "summary": "A concise 2-sentence explanation of the symptoms.",
    "possible_conditions": [
        "Condition Name 1 (Probability %)",
        "Condition Name 2 (Probability %)"
    ],
    "recommended_specialty": "Primary Specialty (e.g., Neurologist, General Physician, Cardiologist)",
    "urgency_level": "Low | Medium | Emergency",
    "emergency_warning": "Action instructions if urgency_level is Emergency, otherwise empty string."
}
"""
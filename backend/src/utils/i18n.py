# src/utils/i18n.py

LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Marathi (मराठी)": "mr",
    "Spanish (Español)": "es"
}

UI_STRINGS = {
    "en": {
        "symptoms_header": "### Describe your symptoms in ANY language by typing or using your microphone! 🎙️",
        "symptoms_label": "Patient Symptoms & Health Context",
        "symptoms_placeholder": "Your spoken words will appear here automatically after recording, or you can type directly...",
        "audio_label": "🎙️ Record or Upload Voice Input (Any Language)",
        "init_triage_btn": "💬 Start Interactive Triage",
        "triage_header": "### 🤖 Follow-Up Clarifying Questions",
        "triage_subheader": "To increase diagnostic precision, please answer these brief questions from Vaiddisha AI:",
        "final_submit_btn": "🩺 Submit Answers & Generate Final Diagnostic Analysis",
        "output_placeholder": "*Diagnostic report will appear here after triage evaluation.*",
        "pdf_label": "📄 Download Official Clinical Report (PDF)",
        "lang_dropdown_label": "🌐 Preferred Language / भाषा चुनें"
    },
    "hi": {
        "symptoms_header": "### किसी भी भाषा में बोलकर या लिखकर अपने लक्षणों का वर्णन करें! 🎙️",
        "symptoms_label": "रोगी के लक्षण और स्वास्थ्य संदर्भ",
        "symptoms_placeholder": "बोलने के बाद आपके शब्द यहाँ अपने आप दिखाई देंगे, या आप सीधे टाइप कर सकते हैं...",
        "audio_label": "🎙️ वॉइस इनपुट रिकॉर्ड या अपलोड करें (किसी भी भाषा में)",
        "init_triage_btn": "💬 इंटरएक्टिव ट्राइएज शुरू करें",
        "triage_header": "### 🤖 AI द्वारा स्पष्टीकरण प्रश्न",
        "triage_subheader": "सटीक निदान के लिए, कृपया वैद दिशा AI के इन प्रश्नों के उत्तर दें:",
        "final_submit_btn": "🩺 उत्तर जमा करें और अंतिम निदान प्राप्त करें",
        "output_placeholder": "*निदान रिपोर्ट यहाँ दिखाई देगी...*",
        "pdf_label": "📄 आधिकारिक नैदानिक रिपोर्ट डाउनलोड करें (PDF)",
        "lang_dropdown_label": "🌐 Preferred Language / भाषा चुनें"
    },
    "mr": {
        "symptoms_header": "### कोणत्याही भाषेत बोलून किंवा टाईप करून तुमच्या लक्षणांचे वर्णन करा! 🎙️",
        "symptoms_label": "रुग्णाची लक्षणे आणि आरोग्य संदर्भ",
        "symptoms_placeholder": "रेकॉर्डिंगनंतर तुमचे शब्द येथे आपोआप दिसतील, किंवा तुम्ही थेट टाईप करू शकता...",
        "audio_label": "🎙️ व्हॉइस इनपुट रेकॉर्ड किंवा अपलोड करा (कोणत्याही भाषेत)",
        "init_triage_btn": "💬 परस्परसंवादी ट्रायज सुरू करा",
        "triage_header": "### 🤖 AI कडून स्पष्टीकरण प्रश्न",
        "triage_subheader": "अचूक निदानासाठी, कृपया वैद्यदिशा AI च्या या प्रश्नांची उत्तरे द्या:",
        "final_submit_btn": "🩺 उत्तरे सबमिट करा आणि अंतिम निदान मिळवा",
        "output_placeholder": "*निदान अहवाल येथे दिसेल...*",
        "pdf_label": "📄 अधिकृत वैद्यकीय अहवाल डाउनलोड करा (PDF)",
        "lang_dropdown_label": "🌐 Preferred Language / भाषा चुनें"
    },
    "es": {
        "symptoms_header": "### ¡Describa sus síntomas en CUALQUIER idioma escribiendo o usando el micrófono! 🎙️",
        "symptoms_label": "Síntomas del paciente y contexto de salud",
        "symptoms_placeholder": "Sus palabras habladas aparecerán aquí automáticamente...",
        "audio_label": "🎙️ Grabar o cargar entrada de voz (Cualquier idioma)",
        "init_triage_btn": "💬 Iniciar triaje interactivo",
        "triage_header": "### 🤖 Preguntas de aclaración de seguimiento",
        "triage_subheader": "Para mayor precisión diagnóstica, responda estas breves preguntas:",
        "final_submit_btn": "🩺 Enviar respuestas y generar análisis de diagnóstico final",
        "output_placeholder": "*El informe de diagnóstico aparecerá aquí...*",
        "pdf_label": "📄 Descargar informe clínico oficial (PDF)",
        "lang_dropdown_label": "🌐 Preferred Language / भाषा चुनें"
    }
}

def get_string(lang_name: str, key: str) -> str:
    """Returns the translated string for a given key, falling back to English."""
    lang_code = LANGUAGES.get(lang_name, "en")
    return UI_STRINGS.get(lang_code, UI_STRINGS["en"]).get(key, UI_STRINGS["en"].get(key, ""))
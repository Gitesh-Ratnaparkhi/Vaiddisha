// frontend/src/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

const resources = {
    en: {
        translation: {
            // Navbar
            symptom_triage: "Symptom Triage",
            lab_vision_ocr: "Lab Vision OCR",
            specialists: "Specialists",
            appointments: "Appointments",
            clinical_decision_support: "Clinical Decision Support",
            sign_out: "Sign Out",

            // Symptom Triage Page
            triage_title: "What symptoms are you experiencing?",
            triage_desc: "Provide as much detail as possible, such as duration, severity, and any triggering factors.",
            symptom_placeholder: "e.g., I have had a dull ache in my lower back for 3 days. It worsens when sitting down...",
            detailed_symptom_desc: "Detailed Symptom Description",
            preferred_report_language: "Preferred Report Language",
            tips_title: "Tips for a better diagnostic prediction:",
            tip_1: "Specify when the symptoms started (e.g. last night, 2 weeks ago).",
            tip_2: "Mention what makes them better or worse (e.g. hot shower, walking, eating).",
            tip_3: "Describe the nature of pain (e.g. sharp, dull ache, throbbing, burning).",
            start_clinical_triage: "Start Clinical Triage",

            // Appointments & Status
            my_bookings: "My Clinical Bookings",
            no_appointments: "No scheduled appointments found.",
            pending: "Pending",
            confirmed: "Confirmed",
            rejected: "Rejected",
            completed: "Completed"
        }
    },
    hi: {
        translation: {
            // Navbar
            symptom_triage: "लक्षण जांच (Triage)",
            lab_vision_ocr: "लैब रिपोर्ट OCR",
            specialists: "विशेषज्ञ डॉक्टर",
            appointments: "अपॉइंटमेंट्स",
            clinical_decision_support: "क्लिनिकल निर्णय सहायता",
            sign_out: "लॉग आउट",

            // Symptom Triage Page
            triage_title: "आप क्या लक्षण महसूस कर रहे हैं?",
            triage_desc: "कृपया अधिक से अधिक विवरण दें, जैसे लक्षण कितने समय से हैं, गंभीरता और कोई ट्रिगर करने वाले कारक।",
            symptom_placeholder: "उदा., मुझे पिछले 3 दिनों से पीठ के निचले हिस्से में हल्का दर्द है। बैठने पर यह बढ़ जाता है...",
            detailed_symptom_desc: "विस्तृत लक्षण विवरण",
            preferred_report_language: "पसंदीदा रिपोर्ट भाषा",
            tips_title: "बेहतर नैदानिक भविष्यवाणी के लिए सुझाव:",
            tip_1: "बताएं कि लक्षण कब शुरू हुए (उदा. कल रात, 2 सप्ताह पहले)।",
            tip_2: "बताएं कि किस चीज से आराम मिलता है या दर्द बढ़ता है (उदा. गर्म पानी, चलना, खाना)।",
            tip_3: "दर्द के प्रकार का वर्णन करें (उदा. तेज, धीमा दर्द, जलन, झनझनाहट)।",
            start_clinical_triage: "क्लिनिकल जांच शुरू करें",

            // Appointments & Status
            my_bookings: "मेरी क्लिनिकल बुकिंग",
            no_appointments: "कोई अपॉइंटमेंट नहीं मिली।",
            pending: "लंबित (Pending)",
            confirmed: "स्वीकृत (Confirmed)",
            rejected: "अस्वीकृत (Rejected)",
            completed: "पूर्ण (Completed)"
        }
    }
};

i18n
    .use(initReactI18next)
    .init({
        resources,
        lng: localStorage.getItem('app_lang') || 'en',
        fallbackLng: 'en',
        interpolation: {
            escapeValue: false
        }
    });

export default i18n;
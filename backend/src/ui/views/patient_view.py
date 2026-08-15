# src/ui/views/patient_view.py
import gradio as gr
from src.utils.i18n import LANGUAGES, UI_STRINGS
from src.services.appointment_service import SLOT_OPTIONS, get_registered_doctor_choices

def render_patient_view():
    """Renders the Patient diagnostic portal with Multilingual support, 2-Way Triage, PDF Export, Analytics, Appointments, and Lab Vision OCR."""
    with gr.Column(visible=False) as patient_container:
        patient_banner = gr.Markdown()

        # Language Selector Bar
        with gr.Row():
            lang_dropdown = gr.Dropdown(
                choices=list(LANGUAGES.keys()),
                value="English",
                label=UI_STRINGS["en"]["lang_dropdown_label"],
                interactive=True,
                scale=1
            )

        with gr.Tabs():
            # TAB 1: TRIAGE & DIAGNOSTICS
            with gr.TabItem("🩺 Diagnostic Triage"):
                header_markdown = gr.Markdown(UI_STRINGS["en"]["symptoms_header"])
                triage_questions_state = gr.State(value=[])

                with gr.Row():
                    with gr.Column(scale=1):
                        audio_input = gr.Audio(
                            sources=["microphone", "upload"], 
                            type="filepath", 
                            format="wav", 
                            label=UI_STRINGS["en"]["audio_label"]
                        )
                        symptoms_input = gr.Textbox(
                            label=UI_STRINGS["en"]["symptoms_label"], 
                            placeholder=UI_STRINGS["en"]["symptoms_placeholder"],
                            lines=4,
                            max_lines=10,
                            elem_id="symptoms-input"
                        )
                        init_triage_btn = gr.Button(UI_STRINGS["en"]["init_triage_btn"], variant="primary", elem_classes=["submit-btn"])

                    with gr.Column(scale=1):
                        output_display = gr.Markdown(
                            value=UI_STRINGS["en"]["output_placeholder"],
                            elem_classes=["result-markdown"],
                            elem_id="analysis-output"
                        )
                        pdf_download_file = gr.File(
                            label=UI_STRINGS["en"]["pdf_label"], 
                            visible=False, 
                            interactive=False
                        )

                with gr.Column(visible=False) as triage_card:
                    gr.Markdown("---")
                    triage_header = gr.Markdown(UI_STRINGS["en"]["triage_header"])
                    triage_subheader = gr.Markdown(UI_STRINGS["en"]["triage_subheader"])
                    
                    q1_box = gr.Radio(choices=[], label="Question 1", visible=False)
                    q2_box = gr.Radio(choices=[], label="Question 2", visible=False)
                    q3_box = gr.Textbox(label="Additional Details", placeholder="Specify duration, severity (1-10)...", lines=2, visible=False)
                    final_submit_btn = gr.Button(UI_STRINGS["en"]["final_submit_btn"], variant="primary", elem_classes=["submit-btn"])

                gr.Examples(
                    examples=[
                        ["Severe chest pain spreading to left arm, sweating, shortness of breath."],
                        ["Dry cough, low-grade fever, fatigue, and loss of taste/smell for 4 days."],
                        ["Red, itchy skin rash with small fluid-filled blisters on my back after gardening."],
                        ["Sudden weakness in my left arm and leg, slight slurring of words for the past hour."]
                    ],
                    inputs=symptoms_input,
                    label="Example Symptoms (Click to fill)"
                )

            # TAB 2: HEALTH HISTORY & ANALYTICS
            with gr.TabItem("📊 Health History & Analytics"):
                history_status_md = gr.Markdown("Click 'Refresh History' to load your past consultations.")
                refresh_history_btn = gr.Button("🔄 Refresh History", variant="secondary")

                with gr.Row():
                    with gr.Column(scale=2):
                        analytics_plot = gr.Plot(label="Triage Risk Distribution")
                    with gr.Column(scale=3):
                        history_dataframe = gr.Dataframe(label="Consultation Records Timeline", interactive=False, wrap=True)

            # TAB 3: BOOK DOCTOR APPOINTMENT
            with gr.TabItem("📅 Book Doctor Appointment"):
                gr.Markdown("### Schedule Consultation with a Medical Specialist")
                with gr.Row():
                    with gr.Column(scale=5):
                        doc_select_dropdown = gr.Dropdown(choices=[], label="Select Specialist / Doctor", interactive=True)
                        reload_docs_btn = gr.Button("🔄 Load Available Doctors", size="sm")
                        
                        app_date_input = gr.Textbox(label="Appointment Date (YYYY-MM-DD)", placeholder="e.g. 2026-08-20")
                        app_slot_dropdown = gr.Dropdown(choices=SLOT_OPTIONS, value=SLOT_OPTIONS[0], label="Select Time Slot", interactive=True)
                        app_reason_input = gr.Textbox(label="Reason for Visit / Symptoms Summary", placeholder="Brief description...", lines=2)
                        
                        book_app_btn = gr.Button("📅 Confirm Appointment Request", variant="primary", elem_classes=["submit-btn"])
                        booking_status_md = gr.Markdown()

                    with gr.Column(scale=6):
                        gr.Markdown("#### 📋 Your Scheduled Appointments")
                        patient_apps_table = gr.Dataframe(label="My Appointments", interactive=False, wrap=True)
                        refresh_my_apps_btn = gr.Button("🔄 Refresh My Appointments", size="sm")

            # TAB 4: MEDICAL DOCUMENT & LAB REPORT ANALYZER (VISION OCR)
            with gr.TabItem("🩻 Lab Report Analyzer"):
                gr.Markdown("### 🔬 Upload Medical Lab Reports, Blood Tests & Diagnostic Documents")
                gr.Markdown("Upload an image of your blood test, lipid panel, or metabolic lab report for instant AI metric extraction and plain-language interpretation.")

                with gr.Row():
                    with gr.Column(scale=10):
                        lab_image_input = gr.Image(
                            sources=["upload", "clipboard"], 
                            type="filepath", 
                            label="📸 Upload Lab Document / Blood Test Image"
                        )
                        lab_notes_input = gr.Textbox(
                            label="Additional Context (Optional)", 
                            placeholder="e.g. Fasting sample taken yesterday, felt dizzy...",
                            lines=2
                        )
                        analyze_lab_btn = gr.Button("🔍 Analyze Lab Report", variant="primary", elem_classes=["submit-btn"])

                    with gr.Column(scale=13):
                        lab_output_display = gr.Markdown(
                            value="*Upload a clear image of your lab report on the left and click 'Analyze Lab Report'.*",
                            elem_classes=["result-markdown"]
                        )

    return (
        patient_container, patient_banner, lang_dropdown, header_markdown, audio_input, symptoms_input, 
        init_triage_btn, output_display, pdf_download_file, triage_card, triage_header, triage_subheader,
        q1_box, q2_box, q3_box, final_submit_btn, triage_questions_state,
        refresh_history_btn, history_dataframe, analytics_plot, history_status_md,
        doc_select_dropdown, reload_docs_btn, app_date_input, app_slot_dropdown, app_reason_input,
        book_app_btn, booking_status_md, patient_apps_table, refresh_my_apps_btn,
        lab_image_input, lab_notes_input, analyze_lab_btn, lab_output_display
    )
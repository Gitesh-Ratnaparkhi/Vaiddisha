# src/ui/views/doctor_view.py
import gradio as gr

def render_doctor_view():
    """Renders the Doctor Consultation Dashboard."""
    with gr.Column(visible=False) as doctor_container:
        doctor_banner = gr.Markdown()
        refresh_btn = gr.Button("🔄 Refresh Patient Consultations", variant="primary")
        consultation_table = gr.Dataframe(
            headers=["ID", "Patient Name", "Symptoms", "Urgency", "Specialty", "Status", "Date"], 
            value=[], 
            interactive=False
        )

    return doctor_container, doctor_banner, refresh_btn, consultation_table
# src/ui/views/patient_view.py
import gradio as gr

def render_patient_view():
    """Renders the Patient diagnostic portal with 2-way interactive triage and PDF export."""
    with gr.Column(visible=False) as patient_container:
        patient_banner = gr.Markdown()
        gr.Markdown("### Describe your symptoms in ANY language by typing or using your microphone! 🎙️")
        
        triage_questions_state = gr.State(value=[])

        # --- STEP 1: INITIAL INPUT SECTION ---
        with gr.Row():
            with gr.Column(scale=1):
                audio_input = gr.Audio(
                    sources=["microphone", "upload"], 
                    type="filepath", 
                    format="wav", 
                    label="🎙️ Record or Upload Voice Input (Any Language)"
                )
                symptoms_input = gr.Textbox(
                    label="Patient Symptoms & Health Context", 
                    placeholder="Your spoken words will appear here automatically after recording, or you can type directly...",
                    lines=4,
                    max_lines=10,
                    elem_id="symptoms-input"
                )
                
                init_triage_btn = gr.Button("💬 Start Interactive Triage", variant="primary", elem_classes=["submit-btn"])

            with gr.Column(scale=1):
                output_display = gr.Markdown(
                    value="*Diagnostic report will appear here after triage evaluation.*",
                    elem_classes=["result-markdown"],
                    elem_id="analysis-output"
                )
                
                # PDF Medical Report Download Component
                pdf_download_file = gr.File(
                    label="📄 Download Official Clinical Report (PDF)", 
                    visible=False, 
                    interactive=False
                )

        # --- STEP 2: DYNAMIC 2-WAY FOLLOW-UP TRIAGE CARD ---
        with gr.Column(visible=False) as triage_card:
            gr.Markdown("---")
            gr.Markdown("### 🤖 Follow-Up Clarifying Questions")
            gr.Markdown("To increase diagnostic precision, please answer these brief questions from Vaiddisha AI:")
            
            q1_box = gr.Radio(choices=[], label="Question 1", visible=False)
            q2_box = gr.Radio(choices=[], label="Question 2", visible=False)
            q3_box = gr.Textbox(label="Additional Details", placeholder="Specify duration, severity (1-10), or additional symptoms...", lines=2, visible=False)
            
            final_submit_btn = gr.Button("🩺 Submit Answers & Generate Final Diagnostic Analysis", variant="primary", elem_classes=["submit-btn"])

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

    return (
        patient_container, patient_banner, audio_input, symptoms_input, 
        init_triage_btn, output_display, pdf_download_file, triage_card, q1_box, q2_box, q3_box, 
        final_submit_btn, triage_questions_state
    )
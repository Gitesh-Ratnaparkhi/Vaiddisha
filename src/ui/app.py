# src/ui/app.py
import gradio as gr
from src.ui.views import render_auth_view, render_terms_view, render_patient_view, render_doctor_view
from src.services.disease_service import process_disease_prediction
from src.services.triage_service import generate_triage_questions
from src.services.audio_service import transcribe_audio
from src.services.auth_service import login_user, register_patient, register_doctor, confirm_terms_acceptance
from src.services.consultation_service import fetch_doctor_consultations

def build_app() -> gr.Blocks:
    with gr.Blocks(title="Vaiddisha - AI Multilingual Medical Portal") as app:
        
        # Header Banner
        gr.HTML(
            """
            <div class="app-header">
                <h1>🩺 Vaiddisha AI</h1>
                <p>Multilingual AI-Powered Clinical Decision-Support & Doctor Portal</p>
            </div>
            """
        )

        user_session = gr.State(value={"logged_in": False, "email": "", "role": "", "name": "", "terms_accepted": False})

        # Render Views
        (
            auth_view, login_email, login_pass, login_btn, login_status,
            p_email, p_pass, p_name, p_gender, p_age, p_country, p_state, p_city, p_postal, p_phone, p_lang, p_conditions, p_surgeries, p_allergies, p_reg_btn, p_reg_status,
            d_email, d_pass, d_name, d_spec, d_qual, d_exp, d_hosp, d_country, d_state, d_city, d_postal, d_phone, d_fee, d_desc, d_reg_btn, d_reg_status
        ) = render_auth_view()

        terms_view, terms_checkbox, accept_terms_btn, terms_status = render_terms_view()
        
        (
            patient_view, patient_banner, audio_input, symptoms_input, 
            init_triage_btn, output_display, pdf_download_file, triage_card, q1_box, q2_box, q3_box, 
            final_submit_btn, triage_questions_state
        ) = render_patient_view()
        
        doctor_view, doctor_banner, refresh_btn, consultation_table = render_doctor_view()

        logout_btn = gr.Button("🚪 Sign Out", variant="stop", visible=False)

        # Controller Handlers
        def handle_login(email, password):
            success, msg, user_info = login_user(email, password)
            if success:
                role = user_info.get("role")
                is_patient = (role == "Patient")
                is_doctor = (role == "Doctor")
                terms_accepted = user_info.get("terms_accepted", False)
                doc_data = fetch_doctor_consultations() if is_doctor else []
                user_name = user_info.get("name")

                session_data = {
                    "logged_in": True, "email": user_info.get("email"), 
                    "role": role, "name": user_name, "terms_accepted": terms_accepted
                }

                if not terms_accepted:
                    return (
                        gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                        "", "", [], session_data, ""
                    )

                return (
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=is_patient), gr.update(visible=is_doctor), gr.update(visible=True),
                    f"## 🩺 Patient Portal — Welcome, {user_name}", f"## 👨‍⚕️ Doctor Dashboard — Dr. {user_name}", doc_data, session_data, ""
                )

            return (
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                "", "", [], {"logged_in": False}, msg
            )

        def handle_accept_terms(session):
            email = session.get("email")
            role = session.get("role")
            user_name = session.get("name")
            
            ok, msg = confirm_terms_acceptance(email)
            if ok:
                session["terms_accepted"] = True
                is_patient = (role == "Patient")
                is_doctor = (role == "Doctor")
                doc_data = fetch_doctor_consultations() if is_doctor else []

                return (
                    gr.update(visible=False), gr.update(visible=is_patient), gr.update(visible=is_doctor), gr.update(visible=True),
                    f"## 🩺 Patient Portal — Welcome, {user_name}", f"## 👨‍⚕️ Doctor Dashboard — Dr. {user_name}", doc_data, session, ""
                )
            return (
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                "", "", [], session, msg
            )

        def handle_logout():
            return (
                gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                {"logged_in": False}
            )

        def start_triage(symptoms, session):
            if not symptoms or not symptoms.strip():
                return (
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    "⚠️ Please enter or record your symptoms before running analysis.",
                    gr.update(visible=False), []
                )

            triage_state = generate_triage_questions(symptoms)
            
            if triage_state.is_complete or not triage_state.followup_questions:
                # Direct prediction
                formatted_md, pdf_path = process_disease_prediction(symptoms, user_session=session)
                return (
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    formatted_md, gr.update(value=pdf_path, visible=bool(pdf_path)), []
                )
            
            questions = triage_state.followup_questions
            q1 = questions[0] if len(questions) > 0 else None
            q2 = questions[1] if len(questions) > 1 else None
            
            q1_update = gr.update(choices=q1.options, label=q1.question, value=None, visible=True) if q1 else gr.update(visible=False)
            q2_update = gr.update(choices=q2.options, label=q2.question, value=None, visible=True) if q2 else gr.update(visible=False)
            q3_update = gr.update(visible=True)
            
            saved_questions = [q.model_dump() for q in questions]
            
            return (
                gr.update(visible=True), q1_update, q2_update, q3_update,
                "💬 *Please answer the clarifying questions below to refine the diagnostic accuracy.*",
                gr.update(visible=False), saved_questions
            )

        def submit_triage(symptoms, q1_ans, q2_ans, q3_ans, saved_questions, session):
            triage_text = ""
            if saved_questions:
                if len(saved_questions) > 0 and q1_ans:
                    triage_text += f"Q: {saved_questions[0]['question']}\nA: {q1_ans}\n\n"
                if len(saved_questions) > 1 and q2_ans:
                    triage_text += f"Q: {saved_questions[1]['question']}\nA: {q2_ans}\n\n"
            if q3_ans and q3_ans.strip():
                triage_text += f"Additional Context: {q3_ans.strip()}"
            
            formatted_md, pdf_path = process_disease_prediction(
                symptoms=symptoms,
                user_session=session,
                triage_answers=triage_text
            )
            
            return (
                gr.update(visible=False),
                formatted_md,
                gr.update(value=pdf_path, visible=bool(pdf_path))
            )

        # Wire handlers
        login_btn.click(
            fn=handle_login, inputs=[login_email, login_pass],
            outputs=[auth_view, terms_view, patient_view, doctor_view, logout_btn, patient_banner, doctor_banner, consultation_table, user_session, login_status]
        )

        accept_terms_btn.click(
            fn=handle_accept_terms, inputs=[user_session],
            outputs=[terms_view, patient_view, doctor_view, logout_btn, patient_banner, doctor_banner, consultation_table, user_session, terms_status]
        )

        p_reg_btn.click(
            fn=register_patient, 
            inputs=[p_email, p_pass, p_name, p_gender, p_age, p_country, p_state, p_city, p_postal, p_phone, p_lang, p_conditions, p_surgeries, p_allergies], 
            outputs=[p_reg_status]
        )
        
        d_reg_btn.click(
            fn=register_doctor, 
            inputs=[d_email, d_pass, d_name, d_spec, d_qual, d_exp, d_hosp, d_country, d_state, d_city, d_postal, d_phone, d_fee, d_desc], 
            outputs=[d_reg_status]
        )

        audio_input.stop_recording(fn=transcribe_audio, inputs=[audio_input], outputs=[symptoms_input])
        audio_input.upload(fn=transcribe_audio, inputs=[audio_input], outputs=[symptoms_input])

        init_triage_btn.click(
            fn=start_triage, 
            inputs=[symptoms_input, user_session], 
            outputs=[triage_card, q1_box, q2_box, q3_box, output_display, pdf_download_file, triage_questions_state]
        )

        final_submit_btn.click(
            fn=submit_triage, 
            inputs=[symptoms_input, q1_box, q2_box, q3_box, triage_questions_state, user_session], 
            outputs=[triage_card, output_display, pdf_download_file]
        )

        refresh_btn.click(fn=fetch_doctor_consultations, outputs=[consultation_table])
        logout_btn.click(fn=handle_logout, outputs=[auth_view, terms_view, patient_view, doctor_view, logout_btn, user_session])

    return app
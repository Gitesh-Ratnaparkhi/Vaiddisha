# src/ui/app.py
import gradio as gr
from src.ui.views import render_auth_view, render_terms_view, render_patient_view, render_doctor_view
from src.services.disease_service import process_disease_prediction
from src.services.triage_service import generate_triage_questions
from src.services.audio_service import transcribe_audio
from src.services.auth_service import login_user, register_patient, register_doctor, confirm_terms_acceptance
from src.services.consultation_service import fetch_doctor_consultations
from src.services.analytics_service import get_patient_history_and_analytics
from src.services.appointment_service import (
    get_registered_doctor_choices, book_new_appointment, 
    fetch_patient_appointments, fetch_doctor_appointment_requests, update_appointment_status
)
from src.services.lab_analyzer_service import analyze_medical_document
from src.exceptions import VaiddishaException
from src.utils.i18n import LANGUAGES, UI_STRINGS
from src.ui.theme import theme, custom_css


def build_app() -> gr.Blocks:
    """Builds and wires up the main Gradio application instance."""
    with gr.Blocks(title="Vaiddisha - AI Multilingual Medical Portal", theme=theme, css=custom_css) as app:
        
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

        # Render Auth & Terms Views
        (
            auth_view, login_email, login_pass, login_btn, login_status,
            p_email, p_pass, p_name, p_gender, p_age, p_country, p_state, p_city, p_postal, p_phone, p_lang, p_conditions, p_surgeries, p_allergies, p_reg_btn, p_reg_status,
            d_email, d_pass, d_name, d_spec, d_qual, d_exp, d_hosp, d_country, d_state, d_city, d_postal, d_phone, d_fee, d_desc, d_reg_btn, d_reg_status
        ) = render_auth_view()

        terms_view, terms_checkbox, accept_terms_btn, terms_status = render_terms_view()
        
        # Render Patient View with Appointments, Analytics & Lab Vision OCR
        (
            patient_view, patient_banner, lang_dropdown, header_markdown, audio_input, symptoms_input, 
            init_triage_btn, output_display, pdf_download_file, triage_card, triage_header, triage_subheader,
            q1_box, q2_box, q3_box, final_submit_btn, triage_questions_state,
            refresh_history_btn, history_dataframe, analytics_plot, history_status_md,
            doc_select_dropdown, reload_docs_btn, app_date_input, app_slot_dropdown, app_reason_input,
            book_app_btn, booking_status_md, patient_apps_table, refresh_my_apps_btn,
            lab_image_input, lab_notes_input, analyze_lab_btn, lab_output_display
        ) = render_patient_view()
        
        # Render Doctor View
        (
            doctor_view, doctor_banner, refresh_consultations_btn, consultation_table,
            doctor_apps_table, refresh_doc_apps_btn, selected_app_id,
            confirm_app_btn, reject_app_btn, complete_app_btn, action_status_md
        ) = render_doctor_view()

        logout_btn = gr.Button("🚪 Sign Out", variant="stop", visible=False)

        # Language Switching Controller
        def change_language(selected_language):
            lang_code = LANGUAGES.get(selected_language, "en")
            strings = UI_STRINGS.get(lang_code, UI_STRINGS["en"])
            return (
                strings["symptoms_header"],
                gr.update(label=strings["audio_label"]),
                gr.update(label=strings["symptoms_label"], placeholder=strings["symptoms_placeholder"]),
                gr.update(value=strings["init_triage_btn"]),
                strings["triage_header"],
                strings["triage_subheader"],
                gr.update(value=strings["final_submit_btn"]),
                gr.update(label=strings["pdf_label"])
            )

        lang_dropdown.change(
            fn=change_language,
            inputs=[lang_dropdown],
            outputs=[
                header_markdown, audio_input, symptoms_input, init_triage_btn,
                triage_header, triage_subheader, final_submit_btn, pdf_download_file
            ]
        )

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
                    return gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), "", "", [], session_data, ""

                return (
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=is_patient), gr.update(visible=is_doctor), gr.update(visible=True),
                    f"## 🩺 Patient Portal — Welcome, {user_name}", f"## 👨‍⚕️ Doctor Dashboard — Dr. {user_name}", doc_data, session_data, ""
                )

            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), "", "", [], {"logged_in": False}, msg

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
            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), "", "", [], session, msg

        def handle_logout():
            return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), {"logged_in": False}

        def handle_triage_step(symptoms):
            if not symptoms or not symptoms.strip():
                return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), [], "⚠️ Please enter or record your symptoms first."

            triage_state = generate_triage_questions(symptoms)
            questions = triage_state.followup_questions

            q1_up = gr.update(visible=False)
            q2_up = gr.update(visible=False)
            q3_up = gr.update(visible=True)

            if len(questions) > 0:
                q1 = questions[0]
                opts = q1.options if q1.options else ["Yes", "No", "Unsure"]
                q1_up = gr.update(label=f"1. {q1.question}", choices=opts, value=opts[0], visible=True)

            if len(questions) > 1:
                q2 = questions[1]
                opts = q2.options if q2.options else ["Mild", "Moderate", "Severe"]
                q2_up = gr.update(label=f"2. {q2.question}", choices=opts, value=opts[0], visible=True)

            return (
                gr.update(visible=True),
                q1_up, q2_up, q3_up,
                questions,
                "💬 *Vaiddisha AI has generated follow-up questions below. Please complete them for maximum accuracy.*"
            )

        def handle_final_prediction_step(symptoms, q1_ans, q2_ans, q3_ans, questions, session, selected_language):
            formatted_answers = []
            if len(questions) > 0 and q1_ans:
                formatted_answers.append(f"{questions[0].question}: {q1_ans}")
            if len(questions) > 1 and q2_ans:
                formatted_answers.append(f"{questions[1].question}: {q2_ans}")
            if q3_ans and q3_ans.strip():
                formatted_answers.append(f"Additional Patient Note: {q3_ans.strip()}")

            triage_context = " | ".join(formatted_answers) if formatted_answers else "None provided"

            formatted_md, pdf_path = process_disease_prediction(
                symptoms=symptoms, 
                user_session=session, 
                triage_answers=triage_context,
                target_language=selected_language
            )

            pdf_update = gr.update(value=pdf_path, visible=True) if pdf_path else gr.update(visible=False)
            return formatted_md, pdf_update

        # Safe Lab Report Vision OCR Handler
        def handle_lab_report_analysis(image_path, patient_notes, target_lang):
            try:
                return analyze_medical_document(image_path, patient_notes, target_lang)
            except VaiddishaException as ve:
                return f"### ❌ Diagnostic Error\n{ve.user_message}"
            except Exception as e:
                return (
                    f"### ❌ Unexpected Error\nAn unexpected issue occurred: {str(e)}."
                    " Please try again."
                )

        # Wire Core UI Listeners
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
            fn=handle_triage_step,
            inputs=[symptoms_input],
            outputs=[triage_card, q1_box, q2_box, q3_box, triage_questions_state, output_display]
        )

        final_submit_btn.click(
            fn=handle_final_prediction_step,
            inputs=[symptoms_input, q1_box, q2_box, q3_box, triage_questions_state, user_session, lang_dropdown],
            outputs=[output_display, pdf_download_file]
        )

        # Patient Health History & Analytics
        refresh_history_btn.click(
            fn=get_patient_history_and_analytics,
            inputs=[user_session],
            outputs=[history_dataframe, analytics_plot, history_status_md]
        )

        # Patient Appointment Booking Listeners
        reload_docs_btn.click(
            fn=lambda: gr.update(choices=get_registered_doctor_choices()),
            outputs=[doc_select_dropdown]
        )

        book_app_btn.click(
            fn=book_new_appointment,
            inputs=[user_session, doc_select_dropdown, app_date_input, app_slot_dropdown, app_reason_input],
            outputs=[booking_status_md]
        )

        refresh_my_apps_btn.click(
            fn=fetch_patient_appointments,
            inputs=[user_session],
            outputs=[patient_apps_table]
        )

        # Lab Report Analyzer Listener (with safe exception handling)
        analyze_lab_btn.click(
            fn=handle_lab_report_analysis,
            inputs=[lab_image_input, lab_notes_input, lang_dropdown],
            outputs=[lab_output_display]
        )

        # Doctor Appointment Approval Workflow Listeners
        refresh_doc_apps_btn.click(
            fn=fetch_doctor_appointment_requests,
            inputs=[user_session],
            outputs=[doctor_apps_table]
        )

        confirm_app_btn.click(
            fn=lambda app_id, sess: update_appointment_status(app_id, "Confirmed", sess),
            inputs=[selected_app_id, user_session],
            outputs=[doctor_apps_table, action_status_md]
        )

        reject_app_btn.click(
            fn=lambda app_id, sess: update_appointment_status(app_id, "Rejected", sess),
            inputs=[selected_app_id, user_session],
            outputs=[doctor_apps_table, action_status_md]
        )

        complete_app_btn.click(
            fn=lambda app_id, sess: update_appointment_status(app_id, "Completed", sess),
            inputs=[selected_app_id, user_session],
            outputs=[doctor_apps_table, action_status_md]
        )

        refresh_consultations_btn.click(fn=fetch_doctor_consultations, outputs=[consultation_table])
        logout_btn.click(fn=handle_logout, outputs=[auth_view, terms_view, patient_view, doctor_view, logout_btn, user_session])

    return app
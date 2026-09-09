# src/ui/views/doctor_view.py
import gradio as gr


def render_doctor_view():
  """Renders the Doctor dashboard with Consultations & Appointment Approval Workflows."""
  with gr.Column(visible=False) as doctor_container:
    doctor_banner = gr.Markdown()

    with gr.Tabs():
      # TAB 1: APPOINTMENTS SCHEDULER & APPROVAL WORKFLOW
      with gr.TabItem("📅 Patient Appointments"):
        gr.Markdown("### 📋 Manage Appointment Requests")
        doctor_apps_table = gr.Dataframe(
            label="Incoming Appointment Requests", interactive=False, wrap=True
        )

        with gr.Row():
          refresh_doc_apps_btn = gr.Button(
              "🔄 Refresh Appointments", variant="secondary"
          )

        with gr.Row():
          with gr.Column(scale=1):
            gr.Markdown("#### ⚡ Quick Actions")
            selected_app_id = gr.Number(
                label="Appointment ID to Update", precision=0
            )
            with gr.Row():
              confirm_app_btn = gr.Button("✅ Confirm Booking", variant="primary")
              reject_app_btn = gr.Button("❌ Reject Booking", variant="stop")
              complete_app_btn = gr.Button(
                  "🎉 Mark Completed", variant="secondary"
              )
            action_status_md = gr.Markdown()

      # TAB 2: CONSULTATION LOGS
      with gr.TabItem("🩺 Recent Consultations"):
        gr.Markdown("### 📜 System-Wide Clinical Consultations")
        refresh_consultations_btn = gr.Button(
            "🔄 Refresh Consultation Logs", variant="secondary"
        )
        consultation_table = gr.Dataframe(
            label="Clinical Consultations Log", interactive=False, wrap=True
        )

  return (
      doctor_container,
      doctor_banner,
      refresh_consultations_btn,
      consultation_table,
      doctor_apps_table,
      refresh_doc_apps_btn,
      selected_app_id,
      confirm_app_btn,
      reject_app_btn,
      complete_app_btn,
      action_status_md,
  )
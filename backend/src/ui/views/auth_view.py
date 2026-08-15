# src/ui/views/auth_view.py
import gradio as gr
from src.utils.location_helper import (
    ALL_COUNTRIES, DEFAULT_COUNTRY, INITIAL_STATES, DEFAULT_STATE, 
    INITIAL_CITIES, DEFAULT_CITY, get_states_for_country, get_cities_for_state
)

def render_auth_view():
    """Renders an attractive, modern Login and Registration portal with location cascades and smooth hover effects."""
    with gr.Column(visible=True, elem_classes=["auth-card"]) as auth_container:
        
        with gr.Tabs(elem_classes=["tab-nav"]):
            
            # --- TAB 1: USER LOGIN ---
            with gr.TabItem("🔐 Sign In"):
                gr.Markdown("### Welcome Back to Vaiddisha AI", elem_classes=["auth-title"])
                gr.Markdown("Sign in to access your diagnostic triage portal and medical history", elem_classes=["auth-subtitle"])
                
                with gr.Row():
                    with gr.Column(scale=1):
                        login_email = gr.Textbox(
                            label="Email Address", 
                            placeholder="e.g. gitesh@gmail.com",
                            type="email"
                        )
                        login_pass = gr.Textbox(
                            label="Password", 
                            placeholder="Enter your secure password", 
                            type="password"
                        )
                        login_btn = gr.Button("🚀 Sign In to Portal", variant="primary", elem_classes=["submit-btn"])
                        login_status = gr.Markdown()

            # --- TAB 2: PATIENT REGISTRATION ---
            with gr.TabItem("🩺 Register as Patient"):
                gr.Markdown("### Create Patient Account", elem_classes=["auth-title"])
                gr.Markdown("Join Vaiddisha AI for personalized multi-language health insights", elem_classes=["auth-subtitle"])
                
                with gr.Row():
                    with gr.Column():
                        p_name = gr.Textbox(label="Full Name*", placeholder="John Doe")
                        p_email = gr.Textbox(label="Email Address*", placeholder="patient@example.com")
                        p_pass = gr.Textbox(label="Password* (Must be > 8 characters)", type="password", placeholder="At least 8 characters")
                        
                        with gr.Row():
                            p_age = gr.Number(label="Age", value=25, precision=0)
                            p_gender = gr.Dropdown(choices=["Male", "Female", "Other"], label="Gender", value="Male")
                        
                        with gr.Row():
                            p_country = gr.Dropdown(choices=ALL_COUNTRIES, label="Country", value=DEFAULT_COUNTRY, filterable=True)
                            p_state = gr.Dropdown(choices=INITIAL_STATES, label="State / Province", value=DEFAULT_STATE, filterable=True)
                        
                        with gr.Row():
                            p_city = gr.Dropdown(choices=INITIAL_CITIES, label="City", value=DEFAULT_CITY, filterable=True)
                            p_postal = gr.Textbox(label="Postal Code / Zip", value="440001")
                    
                    with gr.Column():
                        with gr.Row():
                            p_phone = gr.Textbox(label="Phone Number", placeholder="+91 9876543210")
                            p_lang = gr.Textbox(label="Preferred Language", value="English")
                        
                        p_conditions = gr.Textbox(label="Existing Health Conditions (Optional)", placeholder="e.g. Asthma, Diabetes")
                        p_surgeries = gr.Textbox(label="Previous Surgeries (Optional)", placeholder="e.g. Appendectomy 2020")
                        p_allergies = gr.Textbox(label="Known Allergies (Optional)", placeholder="e.g. Penicillin, Peanuts")
                
                p_reg_btn = gr.Button("📝 Create Patient Account", variant="primary", elem_classes=["submit-btn"])
                p_reg_status = gr.Markdown()

            # --- TAB 3: DOCTOR REGISTRATION ---
            with gr.TabItem("👨‍⚕️ Register as Doctor"):
                gr.Markdown("### Join Doctor Network", elem_classes=["auth-title"])
                gr.Markdown("Register your medical practice to receive nearby patient referrals", elem_classes=["auth-subtitle"])
                
                with gr.Row():
                    with gr.Column():
                        d_name = gr.Textbox(label="Doctor Full Name*", placeholder="Dr. Smith")
                        d_email = gr.Textbox(label="Email Address*", placeholder="dr.smith@hospital.com")
                        d_pass = gr.Textbox(label="Password* (Must be > 8 characters)", type="password")
                        
                        with gr.Row():
                            d_spec = gr.Textbox(label="Specialty*", placeholder="e.g. Cardiologist, Dermatologist")
                            d_qual = gr.Textbox(label="Qualification", placeholder="e.g. MBBS, MD")
                        
                        with gr.Row():
                            d_exp = gr.Textbox(label="Experience", placeholder="e.g. 10 Years")
                            d_fee = gr.Textbox(label="Consultation Fee", placeholder="e.g. ₹500")
                    
                    with gr.Column():
                        d_hosp = gr.Textbox(label="Hospital / Clinic Name", placeholder="City Care Hospital")
                        
                        with gr.Row():
                            d_country = gr.Dropdown(choices=ALL_COUNTRIES, label="Country", value=DEFAULT_COUNTRY, filterable=True)
                            d_state = gr.Dropdown(choices=INITIAL_STATES, label="State / Province", value=DEFAULT_STATE, filterable=True)
                        
                        with gr.Row():
                            d_city = gr.Dropdown(choices=INITIAL_CITIES, label="City", value=DEFAULT_CITY, filterable=True)
                            d_postal = gr.Textbox(label="Postal Code / Zip", value="440001")
                        
                        d_phone = gr.Textbox(label="Contact Phone Number", placeholder="+91 9876543210")

                d_desc = gr.Textbox(
                    label="Doctor Professional Bio / Description (Max 500 words)", 
                    placeholder="Write a brief professional summary, areas of clinical expertise, consultation hours, etc...",
                    lines=3,
                    max_lines=6
                )
                
                d_reg_btn = gr.Button("👨‍⚕️ Register Doctor Profile", variant="primary", elem_classes=["submit-btn"])
                d_reg_status = gr.Markdown()

    # --- LOCATION CASCADE EVENT LISTENERS ---
    p_country.change(fn=get_states_for_country, inputs=[p_country], outputs=[p_state, p_city])
    p_state.change(fn=get_cities_for_state, inputs=[p_country, p_state], outputs=[p_city])

    d_country.change(fn=get_states_for_country, inputs=[d_country], outputs=[d_state, d_city])
    d_state.change(fn=get_cities_for_state, inputs=[d_country, d_state], outputs=[d_city])

    return (
        auth_container, login_email, login_pass, login_btn, login_status,
        p_email, p_pass, p_name, p_gender, p_age, p_country, p_state, p_city, p_postal, p_phone, p_lang, p_conditions, p_surgeries, p_allergies, p_reg_btn, p_reg_status,
        d_email, d_pass, d_name, d_spec, d_qual, d_exp, d_hosp, d_country, d_state, d_city, d_postal, d_phone, d_fee, d_desc, d_reg_btn, d_reg_status
    )
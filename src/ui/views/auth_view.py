# src/ui/views/auth_view.py
import gradio as gr
from src.utils.location_helper import (
    ALL_COUNTRIES, DEFAULT_COUNTRY, INITIAL_STATES, DEFAULT_STATE, 
    INITIAL_CITIES, DEFAULT_CITY, get_states_for_country, get_cities_for_state
)

def render_auth_view():
    with gr.Column(visible=True) as auth_container:
        gr.Markdown("### 🔐 Account Access — Sign In or Register")
        with gr.Row():
            # LOGIN CARD
            with gr.Column(scale=1):
                gr.Markdown("#### 🔑 Sign In")
                login_email = gr.Textbox(label="Email Address", placeholder="e.g. patient@gmail.com")
                login_pass = gr.Textbox(label="Password", type="password", placeholder="Enter your password")
                login_btn = gr.Button("Sign In", variant="primary", elem_classes=["submit-btn"])
                login_status = gr.Markdown()

            # REGISTRATION CARD
            with gr.Column(scale=1):
                gr.Markdown("#### 📝 Register New Account")
                with gr.Tabs():
                    # Patient Tab
                    with gr.TabItem("Register as Patient"):
                        p_name = gr.Textbox(label="Full Name*")
                        p_email = gr.Textbox(label="Email Address*")
                        p_pass = gr.Textbox(label="Password* (Must be > 8 characters)", type="password")
                        
                        with gr.Row():
                            p_age = gr.Number(label="Age", value=25, precision=0)
                            p_gender = gr.Dropdown(["Male", "Female", "Other"], label="Gender", value="Male")
                        
                        with gr.Row():
                            p_country = gr.Dropdown(choices=ALL_COUNTRIES, label="Country", value=DEFAULT_COUNTRY, filterable=True)
                            p_state = gr.Dropdown(choices=INITIAL_STATES, label="State / Province", value=DEFAULT_STATE, filterable=True)
                        
                        with gr.Row():
                            p_city = gr.Dropdown(choices=INITIAL_CITIES, label="City", value=DEFAULT_CITY, filterable=True)
                            p_postal = gr.Textbox(label="Postal Code / Zip")
                        
                        with gr.Row():
                            p_phone = gr.Textbox(label="Phone Number")
                            p_lang = gr.Textbox(label="Preferred Language", value="English")
                        
                        p_conditions = gr.Textbox(label="Existing Health Conditions", placeholder="e.g. Diabetes, Hypertension")
                        p_surgeries = gr.Textbox(label="Previous Surgeries", placeholder="e.g. Appendectomy 2020")
                        p_allergies = gr.Textbox(label="Allergies", placeholder="e.g. Penicillin, Peanuts")
                        
                        p_reg_btn = gr.Button("Register Patient Account", variant="secondary")
                        p_reg_status = gr.Markdown()

                    # Doctor Tab
                    with gr.TabItem("Register as Doctor"):
                        d_name = gr.Textbox(label="Doctor Full Name*")
                        d_email = gr.Textbox(label="Email Address*")
                        d_pass = gr.Textbox(label="Password* (Must be > 8 characters)", type="password")
                        
                        with gr.Row():
                            d_spec = gr.Textbox(label="Speciality*", placeholder="e.g. Cardiologist, Dermatologist")
                            d_qual = gr.Textbox(label="Qualification", placeholder="e.g. MBBS, MD")
                        
                        with gr.Row():
                            d_exp = gr.Textbox(label="Experience", placeholder="e.g. 10 Years")
                            d_fee = gr.Textbox(label="Consultation Fee", placeholder="e.g. $50 / ₹500")
                        
                        d_hosp = gr.Textbox(label="Hospital / Clinic Name")
                        
                        with gr.Row():
                            d_country = gr.Dropdown(choices=ALL_COUNTRIES, label="Country", value=DEFAULT_COUNTRY, filterable=True)
                            d_state = gr.Dropdown(choices=INITIAL_STATES, label="State / Province", value=DEFAULT_STATE, filterable=True)
                        
                        with gr.Row():
                            d_city = gr.Dropdown(choices=INITIAL_CITIES, label="City", value=DEFAULT_CITY, filterable=True)
                            d_postal = gr.Textbox(label="Postal Code / Zip")
                        
                        d_phone = gr.Textbox(label="Contact Phone Number")
                        
                        # Replaced Rating slider with Doctor Description (max 500 words)
                        d_desc = gr.Textbox(
                            label="Doctor Professional Bio / Description (Max 500 words)", 
                            placeholder="Write a brief professional summary, areas of clinical expertise, consultation hours, etc...",
                            lines=4,
                            max_lines=8
                        )
                        
                        d_reg_btn = gr.Button("Register Doctor Profile", variant="secondary")
                        d_reg_status = gr.Markdown()

    p_country.change(fn=get_states_for_country, inputs=[p_country], outputs=[p_state, p_city])
    p_state.change(fn=get_cities_for_state, inputs=[p_country, p_state], outputs=[p_city])

    d_country.change(fn=get_states_for_country, inputs=[d_country], outputs=[d_state, d_city])
    d_state.change(fn=get_cities_for_state, inputs=[d_country, d_state], outputs=[d_city])

    return (
        auth_container, login_email, login_pass, login_btn, login_status,
        p_email, p_pass, p_name, p_gender, p_age, p_country, p_state, p_city, p_postal, p_phone, p_lang, p_conditions, p_surgeries, p_allergies, p_reg_btn, p_reg_status,
        d_email, d_pass, d_name, d_spec, d_qual, d_exp, d_hosp, d_country, d_state, d_city, d_postal, d_phone, d_fee, d_desc, d_reg_btn, d_reg_status
    )
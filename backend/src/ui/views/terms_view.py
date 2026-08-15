# src/ui/views/terms_view.py
import gradio as gr

def render_terms_view():
    """Renders a comprehensive, legally robust Terms of Service and Medical Consent agreement."""
    with gr.Column(visible=False) as terms_container:
        gr.Markdown("## 📄 Terms of Service & Informed Patient Consent")
        gr.Markdown("Please review the complete legal agreement and clinical disclaimers below before accessing the platform.")

        # Scrollable terms box with complete legal protections
        gr.HTML(
            """
            <div style="
                height: 320px; 
                overflow-y: auto; 
                border: 1px solid var(--border-color-primary, #cbd5e1); 
                border-radius: 12px; 
                padding: 1.5rem; 
                background-color: var(--background-fill-secondary, #f8fafc);
                box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.04);
                font-size: 0.9rem;
                line-height: 1.6;
                color: var(--body-text-color, #334155);
            ">
                <h3 style="margin-top: 0; color: #0f172a; font-size: 1.15rem; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem;">
                    VAIDDISHA AI — TERMS OF SERVICE & INFORMED CONSENT AGREEMENT
                </h3>
                <p><em>Last Updated: August 2026</em></p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">1. Medical Disclaimer & Non-Diagnostic Nature</h4>
                <p>Vaiddisha AI operates solely as an artificial intelligence-driven <strong>Clinical Decision-Support Tool (CDST)</strong> designed for informational and educational purposes. The platform analyzes user-submitted symptoms, natural language descriptions, and medical history using probabilistic machine learning models.</p>
                <p><strong>This application DOES NOT render medical diagnoses, formal clinical prognoses, or medical prescriptions.</strong> Information provided by Vaiddisha AI must never replace the clinical judgment, physical examination, or professional consultation of a licensed physician or healthcare provider.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">2. Emergency Medical Protocol</h4>
                <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.1rem; border-radius: 6px; margin: 0.75rem 0;">
                    <strong style="color: #991b1b; font-size: 0.95rem;">🚨 CRITICAL MEDICAL EMERGENCY NOTICE:</strong>
                    <p style="color: #7f1d1d; margin: 0.3rem 0 0 0; font-weight: 500;">
                        If you are experiencing life-threatening symptoms—including severe chest pain, sudden numbness or weakness, difficulty breathing, slurred speech, acute abdominal pain, or severe trauma—<strong>DO NOT USE THIS APPLICATION</strong>. Immediately contact local emergency services (e.g., 112 / 911 / 102) or proceed to the nearest hospital emergency department.
                    </p>
                </div>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">3. AI Technology Limitations & Output Variability</h4>
                <p>Artificial intelligence language models generate probabilistic outputs based on patterns in training data. Consequently, outputs may occasionally contain incomplete, inaccurate, or outdated medical information ("hallucinations"). You acknowledge and accept that medical risk scores, urgency rankings, and symptom summaries are automated estimates and should be independently validated by a qualified clinician.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">4. Privacy, Data Protection & Informed Consent</h4>
                <p>By accepting these terms, you grant explicit consent for Vaiddisha AI to store and process your personal details, audio recordings, transcribed symptoms, and historical health records. Data processing adheres to the following standards:</p>
                <ul style="padding-left: 1.25rem;">
                    <li><strong>Clinical Records:</strong> Consultation records are stored securely in encrypted databases to facilitate seamless reviews during doctor appointments.</li>
                    <li><strong>Audio Processing:</strong> Voice inputs are transcribed locally or via secure processing pipelines for symptom extraction.</li>
                    <li><strong>No Third-Party Sale:</strong> Your protected personal and medical information will never be sold, leased, or transmitted to third-party marketing brokers.</li>
                </ul>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">5. Doctor Directory & Specialist Recommendation Disclaimer</h4>
                <p>Specialist recommendations and doctor directory listings presented by Vaiddisha AI are populated based on matching medical specialties, geographic location, and availability ratings. The inclusion of a practitioner on this platform:</p>
                <ul style="padding-left: 1.25rem;">
                    <li>Does not constitute a endorsement, warranty, or guarantee of medical competence by Vaiddisha AI.</li>
                    <li>Does not establish a formal doctor-patient relationship until an independent medical consultation occurs outside this automated triage tool.</li>
                </ul>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">6. Limitation of Liability & Indemnification</h4>
                <p>To the fullest extent permitted by applicable law, Vaiddisha AI, its creators, operators, software architects, and data providers shall not be held liable for any direct, indirect, consequential, special, or exemplary damages—including personal injury, wrongful death, delayed treatment, or lost data—arising out of or related to your reliance on the AI-generated analysis or software operation.</p>
                <p>You agree to defend, indemnify, and hold harmless the platform operators from any claims, liabilities, or expenses resulting from your misuse of the platform or violation of these Terms.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">7. User Duty of Accuracy</h4>
                <p>You agree to provide accurate, complete, and truthful information regarding your age, gender, medical history, existing conditions, and symptoms. Providing false or incomplete data directly compromises the safety and validity of the diagnostic support pipeline.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">8. Intellectual Property Rights</h4>
                <p>All software algorithms, user interface designs, logos, and proprietary AI prompts associated with Vaiddisha AI are the exclusive intellectual property of the project developers and protected under copyright and trademark laws.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">9. Modifications to Agreement</h4>
                <p>We reserve the right to update or modify these Terms of Service at any time. Continued usage of the platform following modifications constitutes acceptance of the revised terms.</p>

                <h4 style="color: #0f172a; font-size: 1rem; margin-top: 1.25rem;">10. Governing Law</h4>
                <p>This agreement shall be governed by and construed in accordance with applicable regional healthcare software directives and digital privacy regulations.</p>
            </div>
            """
        )

        with gr.Row():
            terms_checkbox = gr.Checkbox(
                label="I have thoroughly read, understood, and voluntarily agree to all 10 sections of the Terms of Service and Medical Consent Agreement.", 
                value=False,
                interactive=True
            )

        with gr.Row():
            accept_terms_btn = gr.Button(
                "Accept Agreement & Proceed to Portal", 
                variant="primary", 
                interactive=False, 
                elem_classes=["submit-btn"]
            )

        terms_status = gr.Markdown()

    # Enable acceptance button only after checking the consent checkbox
    terms_checkbox.change(
        fn=lambda checked: gr.update(interactive=checked),
        inputs=[terms_checkbox],
        outputs=[accept_terms_btn]
    )

    return terms_container, terms_checkbox, accept_terms_btn, terms_status
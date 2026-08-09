# src/ui/theme.py
import gradio as gr

theme = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="blue",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Outfit"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("Fira Code"), "ui-monospace", "SFMono-Regular", "monospace"],
).set(
    body_background_fill="*neutral_50",
    body_background_fill_dark="*neutral_950",
    button_primary_background_fill="linear-gradient(90deg, #0d9488 0%, #2563eb 100%)",
    button_primary_background_fill_hover="linear-gradient(90deg, #0f766e 0%, #1d4ed8 100%)",
    button_primary_text_color="white",
    block_radius="16px",
    block_shadow="0 4px 20px -2px rgba(0, 0, 0, 0.05)",
    block_shadow_dark="0 4px 20px -2px rgba(0, 0, 0, 0.5)",
)

custom_css = """
.app-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    padding: 2rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    color: white;
    text-align: center;
    box-shadow: 0 10px 30px -10px rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
.app-header h1 {
    font-size: 2.3rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(90deg, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.app-header p {
    font-size: 1.05rem;
    color: #94a3b8;
    margin: 0;
}
.submit-btn {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px -6px rgba(13, 148, 136, 0.4);
}
.result-markdown {
    background: var(--block-background-fill);
    border: 1px solid var(--block-border-color);
    padding: 1.5rem !important;
    border-radius: 12px !important;
}
"""
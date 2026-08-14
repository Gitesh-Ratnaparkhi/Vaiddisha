from gradio.themes import Soft, GoogleFont

# Custom Gradio Theme
theme = Soft(
    primary_hue="teal",
    secondary_hue="slate",
    neutral_hue="slate",
    font=[GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
)

# Custom Modern CSS with Glassmorphism, Shadows, and Smooth Hover Effects
custom_css = """
/* App Global Header Banner */
.app-header {
    background: linear-gradient(135deg, #0f172a 0%, #0d9488 100%);
    color: #ffffff;
    padding: 24px 30px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0 10px 25px -5px rgba(13, 148, 136, 0.3);
    text-align: center;
}

.app-header h1 {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.app-header p {
    font-size: 1.05rem;
    opacity: 0.9;
    font-weight: 400;
}

/* Auth View Glassmorphism Card Container */
.auth-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.auth-card:hover {
    box-shadow: 0 25px 50px -12px rgba(13, 148, 136, 0.15);
    border-color: #cbd5e1;
}

/* Form Headings */
.auth-title {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #0f172a !important;
    margin-bottom: 8px !important;
    text-align: center;
}

.auth-subtitle {
    font-size: 0.92rem !important;
    color: #64748b !important;
    text-align: center;
    margin-bottom: 20px !important;
}

/* Input Fields & Textboxes */
.gr-textbox input, .gr-textbox textarea {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    padding: 12px 16px !important;
    transition: all 0.25s ease-in-out !important;
    background-color: #f8fafc !important;
}

.gr-textbox input:focus, .gr-textbox textarea:focus {
    border-color: #0d9488 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.12) !important;
}

/* Primary Action Buttons with Glow Hover Effect */
.submit-btn {
    background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    cursor: pointer !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25) !important;
}

.submit-btn:hover {
    transform: translateY(-2px) scale(1.01) !important;
    background: linear-gradient(135deg, #0f766e 0%, #115e59 100%) !important;
    box-shadow: 0 8px 20px rgba(13, 148, 136, 0.4) !important;
}

.submit-btn:active {
    transform: translateY(0) scale(0.99) !important;
}

/* Tab Switching Modern Styling */
.tab-nav button {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: #64748b !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
    padding: 10px 16px !important;
}

.tab-nav button:hover {
    color: #0d9488 !important;
    background: #f1f5f9 !important;
}

.tab-nav button.selected {
    color: #0d9488 !important;
    border-bottom: 3px solid #0d9488 !important;
    background: #f0fdf4 !important;
}
"""
# main.py
from src.ui.app import build_app
from src.ui.theme import theme, custom_css

if __name__ == "__main__":
    app = build_app()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=theme,
        css=custom_css,
        inbrowser=True
    )
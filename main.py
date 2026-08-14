# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from src.api.router import api_v1_router
from src.ui.app import build_app

# 1. Initialize FastAPI Application
app = FastAPI(
    title="Vaiddisha AI - Medical REST API",
    description="Multilingual AI Clinical Decision-Support & Doctor Portal REST APIs",
    version="1.0.0"
)

# 2. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Mount all API v1 Endpoints
app.include_router(api_v1_router)

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "online", "service": "Vaiddisha AI Medical Platform"}

# 4. Build Gradio UI and Mount it to FastAPI at "/"
gradio_interface = build_app()
app = gr.mount_gradio_app(app, gradio_interface, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7861)
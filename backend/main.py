# backend/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import api_v1_router
from src.repositories.database import init_db

# Initialize database schema
init_db()

app = FastAPI(
    title="Vaiddisha AI - Medical REST API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Vaiddisha AI Clinical Backend",
        "docs_url": "/docs"
    }

# Mount API routes
app.include_router(api_v1_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=7861, reload=True)
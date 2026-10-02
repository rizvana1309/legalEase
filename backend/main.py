from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-assisted legal document drafting API for LegalEase.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["health"])
def root():
    return {
        "app": settings.app_name,
        "status": "running",
        "ai_enabled": settings.ai_enabled,
        "model": settings.gemini_model if settings.ai_enabled else "demo-mode",
    }


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "ai_enabled": settings.ai_enabled}

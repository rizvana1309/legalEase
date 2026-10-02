from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.config import get_settings
from backend.schemas import DocumentRequest, DocumentResponse

router = APIRouter(prefix="/api", tags=["documents"])
settings = get_settings()
generator = GeminiDocumentGenerator(settings)

DISCLAIMER = (
    "LegalEase generates AI-assisted drafts for informational and drafting purposes. "
    "It is not legal advice. Review the document with a qualified legal professional before signing or relying on it."
)


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        content = generator.generate_document(request)
        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=settings.gemini_model if settings.ai_enabled else "demo-mode",
            demo_mode=not settings.ai_enabled,
            disclaimer=DISCLAIMER,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unexpected generation error: {exc}") from exc

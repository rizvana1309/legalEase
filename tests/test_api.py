import os

os.environ["DEMO_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_demo_document():
    payload = {
        "document_type": "Non-Disclosure Agreement",
        "parties": "Jane Doe (Disclosing Party), ABC Ltd (Receiving Party)",
        "terms": "Confidentiality for 2 years; no disclosure to third parties; return confidential information on request",
        "effective_date": "10/04/2026",
        "additional_instructions": "Include signature blocks.",
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["demo_mode"] is True
    assert "NON-DISCLOSURE AGREEMENT" in data["content"]


def test_validation():
    response = client.post("/api/generate", json={"document_type": "NDA"})
    assert response.status_code == 422

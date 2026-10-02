# LegalEase — AI-Powered Legal Document Generator

LegalEase is a FastAPI + Streamlit application for generating editable legal-document drafts with Gemini, previewing them, and exporting them as TXT, DOCX, or PDF.

## Architecture

```text
Streamlit UI (frontend/app.py)
        |
        | POST /api/generate
        v
FastAPI (backend/main.py + routes.py)
        |
        v
GeminiDocumentGenerator
        |
        v
Google Gemini API

Local export:
Streamlit -> TXT / python-docx -> DOCX / fpdf2 -> PDF
```

The application intentionally does not store submitted legal data in a database. Generation happens per request, which is a safer local-development default for sensitive drafts.

## Requirements

- Python 3.10+
- A Gemini API key for real AI generation
- VS Code recommended

## Windows + VS Code setup

Open the project folder in VS Code, then open **Terminal > New Terminal**.

### 1. Create a virtual environment

PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
py -3 -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create `.env`

Copy `.env.example` to `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
```

Then edit `.env`:

```env
GEMINI_API_KEY=YOUR_KEY_HERE
GEMINI_MODEL=gemini-2.5-flash
DEMO_MODE=false
BACKEND_URL=http://127.0.0.1:8000
APP_NAME=LegalEase
COMPANY_NAME=LegalEase
```

If you want to test the complete UI without an API key first, use:

```env
GEMINI_API_KEY=
DEMO_MODE=true
```

Demo mode still exercises the API, editor, preview, and exports, but it does not call Gemini.

## Run the application

Use **two VS Code terminals**.

### Terminal 1 — FastAPI

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

### Terminal 2 — Streamlit

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Streamlit will print a local URL, normally `http://localhost:8501`.

## How to test

1. Enter a document type, such as `Freelance Work Contract`.
2. Enter parties, for example `Jane Doe (Service Provider), TechNova Inc. (Client)`.
3. Enter semicolon-separated terms.
4. Enter the effective date.
5. Click **Generate Document**.
6. Edit the generated text in the left editor.
7. Verify the live preview on the right.
8. Download TXT, DOCX, and PDF and open each file.

## API example

```http
POST /api/generate
Content-Type: application/json
```

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), ABC Ltd (Receiving Party)",
  "terms": "Confidentiality for 2 years; no disclosure to third parties; return confidential information on request",
  "effective_date": "10/04/2026",
  "additional_instructions": "Include signature blocks."
}
```

## Project structure

```text
LegalEase/
├── assets/
│   ├── logo.png
│   └── logo.svg
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   ├── config.py
│   ├── ai_core/
│   │   ├── __init__.py
│   │   └── gemini_generator.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── document_service.py
│   └── utils/
│       ├── __init__.py
│       └── text.py
├── frontend/
│   └── app.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── Procfile
├── README.md
└── requirements.txt
```

## Important implementation notes

- The original specification names `gemini-1.5-pro` and `google-generativeai`. Those are retained in the documentation as the historical project choice, but the implementation uses Google's newer `google-genai` SDK and a configurable current model so the application is not tied to a legacy SDK.
- The default model is configurable through `GEMINI_MODEL`. If your Google AI Studio account exposes a different model, change that one environment variable instead of changing application code.
- The application includes a demo mode so the complete frontend/backend/export workflow can be tested before configuring an API key.
- The PDF exporter uses standard PDF fonts and replaces unsupported Unicode punctuation with safe equivalents. DOCX preserves normal Unicode text better.
- The application does not claim that generated documents are legally valid or attorney-reviewed.

## Production checklist

Before public deployment, add authentication, rate limiting, encrypted/controlled logging, secret management, HTTPS, audit policies, explicit retention/deletion controls, jurisdiction-aware legal review, and stronger document validation. Do not expose a Gemini API key in frontend code.

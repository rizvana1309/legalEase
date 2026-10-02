import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
import os
from html import escape

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from backend.services.document_service import format_docx, format_pdf, format_txt
from backend.utils.text import html_preview, sanitize_text

st.set_page_config(
    page_title="LegalEase | AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown(
    """
    <style>
    .hero { padding: 1.2rem 1.4rem; border-radius: 18px; background: linear-gradient(135deg,#0b1f3a,#164e63); color:white; }
    .hero h1 { margin:0; font-size:2.25rem; }
    .hero p { margin:.35rem 0 0; color:#dbeafe; }
    .preview { background:#111827; color:#f3f4f6; padding:24px; border-radius:14px; max-height:620px; overflow-y:auto; line-height:1.65; }
    .preview h3 { color:#93c5fd; margin-top:20px; }
    .preview p { margin:0 0 10px; }
    .notice { padding:12px 16px; border-left:4px solid #f59e0b; background:#fffbeb; border-radius:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>⚖️ LegalEase</h1><p>AI-powered legal document drafting with editable previews and branded exports.</p></div>',
    unsafe_allow_html=True,
)

st.caption("Drafting assistant only — not a substitute for qualified legal advice.")

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = "Legal Document"

with st.sidebar:
    st.header("Document details")
    document_type = st.text_input("Document type", placeholder="e.g. Non-Disclosure Agreement")
    parties = st.text_area(
        "Parties involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=110,
    )
    terms = st.text_area(
        "Terms & conditions",
        placeholder="Payment within 30 days; confidentiality maintained; either party may terminate with 15 days notice",
        height=180,
        help="Use semicolons to separate major terms, as specified in the project documentation.",
    )
    effective_date = st.text_input("Effective date", placeholder="e.g. 10/04/2026")
    additional = st.text_area(
        "Additional instructions (optional)",
        placeholder="Use a formal tone and include signature blocks.",
        height=100,
    )

    generate = st.button("Generate Document", type="primary", use_container_width=True)

    st.divider()
    st.caption(f"Backend: {BACKEND_URL}")
    if st.button("Clear document", use_container_width=True):
        st.session_state.document = ""
        st.rerun()

if generate:
    missing = []
    for label, value in [
        ("Document type", document_type),
        ("Parties", parties),
        ("Terms", terms),
        ("Effective date", effective_date),
    ]:
        if not value.strip():
            missing.append(label)

    if missing:
        st.error("Please fill in: " + ", ".join(missing))
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date,
            "additional_instructions": additional,
        }
        with st.spinner("Generating your draft..."):
            try:
                response = requests.post(f"{BACKEND_URL}/api/generate", json=payload, timeout=90)
                if response.ok:
                    data = response.json()
                    st.session_state.document = data["content"]
                    st.session_state.generated_type = data["document_type"]
                    if data.get("demo_mode"):
                        st.warning("Demo mode is active. Add GEMINI_API_KEY to .env and set DEMO_MODE=false for real Gemini generation.")
                    else:
                        st.success(f"Generated with {data.get('model', 'Gemini')}")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error ({response.status_code}): {detail}")
            except requests.RequestException as exc:
                st.error(f"Could not reach FastAPI at {BACKEND_URL}. Start the backend first. Details: {exc}")

left, right = st.columns([1.25, 1], gap="large")

with left:
    st.subheader("Editable document")
    edited = st.text_area(
        "Edit the generated content before exporting",
        value=st.session_state.document,
        height=650,
        label_visibility="collapsed",
        placeholder="Your generated legal document will appear here...",
    )
    if edited != st.session_state.document:
        st.session_state.document = edited

with right:
    st.subheader("Live preview")
    if st.session_state.document.strip():
        st.markdown(
            f'<div class="preview">{html_preview(st.session_state.document)}</div>',
            unsafe_allow_html=True,
        )

        content = sanitize_text(st.session_state.document)
        base_name = "legalease_document"
        st.download_button(
            "Download TXT",
            data=format_txt(content),
            file_name=f"{base_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )
        st.download_button(
            "Download DOCX",
            data=format_docx(content, st.session_state.generated_type, terms),
            file_name=f"{base_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
        st.download_button(
            "Download PDF",
            data=format_pdf(content, st.session_state.generated_type),
            file_name=f"{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.info("Generate a document to see the formatted preview and export buttons.")

st.divider()
st.markdown(
    '<div class="notice"><strong>Legal review notice:</strong> AI output can contain omissions or errors. Verify facts, jurisdiction-specific requirements, and final wording with a qualified legal professional before signing or relying on a document.</div>',
    unsafe_allow_html=True,
)

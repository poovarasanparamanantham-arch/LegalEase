import os
from datetime import date
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.exporters import format_docx, format_pdf, text_to_txt, format_html_preview

load_dotenv()

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.markdown(
    """
    <style>
    .hero { text-align:center; padding: 1rem 0 0.5rem; }
    .hero h1 { margin-bottom:0.1rem; }
    .preview {
        background:#111827; color:#f9fafb; padding:24px;
        border-radius:12px; max-height:620px; overflow-y:auto;
        line-height:1.65; font-family: Georgia, serif;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><h1>⚖️ LegalEase</h1>'
    '<p>AI-powered legal document drafting and export</p></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    backend_url = st.text_input("Backend URL", BACKEND_URL)
    jurisdiction = st.text_input("Jurisdiction", "India")
    logo_file = st.file_uploader("Optional logo", type=["png", "jpg", "jpeg"])

    st.info(
        "LegalEase is a drafting aid, not a substitute for advice from a qualified legal professional."
    )

document_type = st.selectbox(
    "Document Type",
    [
        "Employment Contract",
        "Non-Disclosure Agreement",
        "Lease Agreement",
        "Freelance Work Contract",
        "Service Agreement",
        "General Agreement",
        "Custom Legal Document",
    ],
)

col1, col2 = st.columns(2)

with col1:
    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=140,
    )
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment to be made within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=220,
    )

with col2:
    effective_date = st.date_input("Effective Date", value=date.today())
    additional_instructions = st.text_area(
        "Additional Instructions (optional)",
        placeholder="Add special drafting requirements or placeholders.",
        height=140,
    )
    st.caption("Separate terms with semicolons, as specified in the project documentation.")

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = document_type

if st.button("✨ Generate Document", type="primary", use_container_width=True):
    if not parties.strip() or not terms.strip():
        st.error("Please provide the parties and at least one term.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": effective_date.isoformat(),
            "jurisdiction": jurisdiction,
            "additional_instructions": additional_instructions,
        }
        with st.spinner("Generating your document..."):
            try:
                response = requests.post(
                    f"{backend_url}/generate",
                    json=payload,
                    timeout=120,
                )
                response.raise_for_status()
                data = response.json()
                st.session_state.document = data["content"]
                st.session_state.generated_type = data["document_type"]
                st.success(f"Generated with {data.get('model', 'configured Gemini model')}.")
            except requests.RequestException as exc:
                st.error(f"Could not reach the backend: {exc}")
            except (KeyError, ValueError) as exc:
                st.error(f"Unexpected backend response: {exc}")

if st.session_state.document:
    st.divider()
    st.subheader("Document Preview")

    edited = st.text_area(
        "Edit Document",
        value=st.session_state.document,
        height=520,
        key="editable_document",
    )
    st.session_state.document = edited

    st.markdown(
        f'<div class="preview">{format_html_preview(edited)}</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Download")
    d1, d2, d3 = st.columns(3)

    txt_bytes = text_to_txt(edited)
    docx_bytes = format_docx(edited, st.session_state.generated_type)
    pdf_bytes = format_pdf(edited, st.session_state.generated_type)

    base_name = st.session_state.generated_type.lower().replace(" ", "_")

    with d1:
        st.download_button(
            "⬇️ Download TXT",
            data=txt_bytes,
            file_name=f"{base_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with d2:
        st.download_button(
            "⬇️ Download DOCX",
            data=docx_bytes,
            file_name=f"{base_name}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with d3:
        st.download_button(
            "⬇️ Download PDF",
            data=pdf_bytes,
            file_name=f"{base_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

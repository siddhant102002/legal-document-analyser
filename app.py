import streamlit as st
import tempfile
import os
from datetime import datetime
from document_reader import extract_text
from analyser import summarise_contract, identify_clauses, flag_risks, suggest_questions
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="AI Legal Document Analyser",
    page_icon="⚖️",
    layout="wide"
)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.title("How to use")
    st.markdown("""
1. Upload a contract (PDF or Word)
2. Click Analyse Contract
3. Review the 4 analysis tabs
4. Download your full report

Supported document types:
- Non-Disclosure Agreements (NDA)
- Employment Contracts
- Service Agreements
- Rental / Lease Agreements
- Freelance Contracts
- Any standard legal contract
""")
    st.divider()
    st.warning("""
Disclaimer

This tool provides AI-generated analysis for informational purposes only.

It is not legal advice. Always consult a qualified solicitor before signing any contract.
""")
    st.divider()
    st.caption("Built by Siddhant Tayade · Powered by Gemini AI")

# ── Contract type detection (Gemini) ──────────────────────────
def detect_contract_type(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Look at the first part of this contract and identify what type it is.

Reply with ONLY the contract type name.

Examples:
- Non-Disclosure Agreement
- Employment Contract
- Service Agreement
- Rental Agreement
- Freelance Contract

Contract start:
{text[:500]}
"""
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception:
        return "Legal Contract"

# ── Main UI ───────────────────────────────────────────────────
st.title("AI Legal Document Analyser")
st.markdown("Powered by Gemini AI · Upload any contract for instant analysis")

uploaded_file = st.file_uploader(
    "Upload your contract (PDF or Word)",
    type=["pdf", "docx"]
)

if uploaded_file and st.button("Analyse Contract", type="primary"):

    # ── Save file temporarily ─────────────────────────────────
    try:
        suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".docx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
    except Exception as e:
        st.error(f"Could not save file: {e}")
        st.stop()

    # ── Extract text ──────────────────────────────────────────
    try:
        text = extract_text(temp_path)
        text = " ".join(text.split())
    except Exception as e:
        st.error(f"Could not read document: {e}")
        st.stop()
    finally:
        os.unlink(temp_path)

    # ── File size check ───────────────────────────────────────
    truncated = False
    if len(text) > 8000:
        text = text[:8000]
        truncated = True

    if truncated:
        st.info("Document is very long. Analysing first portion.")

    if len(text) < 50:
        st.error("Could not extract enough text from this document. Please try a different file.")
        st.stop()

    # ── Contract type detection ───────────────────────────────
    contract_type = detect_contract_type(text)
    st.success(f"This appears to be a {contract_type}")
    st.caption(f"Document: {uploaded_file.name} · Analysed on {datetime.now().strftime('%d %B %Y at %H:%M')}")
    st.divider()

    # ── Progress bar + analysis ───────────────────────────────
    progress = st.progress(0, text="Starting analysis...")

    try:
        progress.progress(10, text="Summarising contract...")
        summary = summarise_contract(text)

        progress.progress(35, text="Identifying key clauses...")
        clauses = identify_clauses(text)

        progress.progress(60, text="Flagging risks...")
        risks = flag_risks(text)

        progress.progress(85, text="Generating questions...")
        questions = suggest_questions(text)

        progress.progress(100, text="Analysis complete!")

    except Exception as e:
        st.error("Analysis failed. Please try again.")
        st.caption(f"Error detail: {e}")
        st.stop()

    # ── Results tabs ──────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "Summary",
        "Key Clauses",
        "Risk Flags",
        "Questions to Ask"
    ])

    with tab1:
        st.markdown(summary)

    with tab2:
        st.markdown(clauses)

    with tab3:
        st.warning(risks)

    with tab4:
        st.markdown(questions)

    # ── Download report ───────────────────────────────────────
    full_report = f"""AI LEGAL DOCUMENT ANALYSER — FULL REPORT

Document: {uploaded_file.name}
Contract type: {contract_type}
Analysed on: {datetime.now().strftime('%d %B %Y at %H:%M')}

DISCLAIMER:
This is AI-generated analysis for informational purposes only.
It is not legal advice.

----------------------------------------
SUMMARY
----------------------------------------
{summary}

----------------------------------------
KEY CLAUSES
----------------------------------------
{clauses}

----------------------------------------
RISK FLAGS
----------------------------------------
{risks}

----------------------------------------
QUESTIONS TO ASK BEFORE SIGNING
----------------------------------------
{questions}

----------------------------------------
Generated by AI Legal Document Analyser
Powered by Gemini AI
"""

    st.divider()
    st.download_button(
        label="Download Full Report",
        data=full_report,
        file_name=f"analysis_{uploaded_file.name.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
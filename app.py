import streamlit as st
import tempfile
from document_reader import extract_text
from analyser import summarise_contract, identify_clauses, flag_risks, suggest_questions

st.title("⚖️ AI Legal Document Analyser")
st.markdown("Powered by Groq AI · Upload any contract for instant analysis")

uploaded_file = st.file_uploader(
    "Upload your contract (PDF or Word)",
    type=["pdf", "docx"]
)

if uploaded_file and st.button("Analyse Contract", type="primary"):

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    with st.spinner("AI is analysing your contract..."):

        # Extract text
        text = extract_text(temp_path)

        # Clean text
        text = " ".join(text.split())

        # Limiting text size to avoid token error
        text = text[:2000]

        # Run analysis
        summary = summarise_contract(text)
        clauses = identify_clauses(text)
        risks = flag_risks(text)
        questions = suggest_questions(text)

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Summary",
        "🔍 Key Clauses",
        "🚨 Risk Flags",
        "❓ Questions"
    ])

    with tab1:
        st.markdown(summary)

    with tab2:
        st.markdown(clauses)

    with tab3:
        st.error(risks)

    with tab4:
        st.markdown(questions)

    # Download report
    full_report = f"""
===== SUMMARY =====
{summary}

===== KEY CLAUSES =====
{clauses}

===== RISKS =====
{risks}

===== QUESTIONS =====
{questions}
"""

    st.download_button(
        "📥 Download Full Report",
        full_report,
        file_name="contract_analysis.txt"
    )
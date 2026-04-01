import streamlit as st
import tempfile
import os
from datetime import datetime
import anthropic
from dotenv import load_dotenv
from document_reader import extract_text
from analyser import detect_contract_type, analyse_all

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=api_key)
MODEL = "claude-sonnet-4-5"

st.set_page_config(
    page_title="AI Legal Document Analyser",
    page_icon="⚖️",
    layout="wide"
)

with st.sidebar:
    st.title("⚖️ How to use")
    st.markdown("""
1. Upload a contract (PDF or Word)
2. Click Analyse Contract
3. Review the 4 analysis tabs
4. Chat with your contract
5. Download your full report

**Supported document types:**
- Non-Disclosure Agreements (NDA)
- Employment Contracts
- Service Agreements
- Rental / Lease Agreements
- Freelance Contracts
- Any standard legal contract
""")
    st.divider()
    st.warning("""
**Disclaimer**

This tool provides AI-generated analysis for informational purposes only.

It is not legal advice. Always consult a qualified solicitor before signing any contract.
""")
    st.divider()
    st.caption("Built by Siddhant Tayade · Powered by Claude AI")


st.title("⚖️ AI Legal Document Analyser")
st.markdown("**Powered by Claude AI** · Upload any contract for instant analysis")

uploaded_file = st.file_uploader(
    "Upload your contract (PDF or Word)",
    type=["pdf", "docx"]
)

if uploaded_file and st.button("Analyse Contract", type="primary"):

    try:
        suffix = ".pdf" if uploaded_file.name.lower().endswith(".pdf") else ".docx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name
    except Exception as e:
        st.error(f"Could not save file: {e}")
        st.stop()

    try:
        text = extract_text(temp_path)
        text = " ".join(text.split())
    except Exception as e:
        st.error(f"Could not read document: {e}")
        st.stop()
    finally:
        os.unlink(temp_path)

    if len(text) < 50:
        st.error("Could not extract enough text. Please try a different file.")
        st.stop()

    st.session_state["contract_text"] = text

    with st.spinner("Detecting contract type..."):
        contract_type = detect_contract_type(text)

    st.success(f"✅ This appears to be a **{contract_type}**")
    st.caption(f"Document: {uploaded_file.name} · Analysed on {datetime.now().strftime('%d %B %Y at %H:%M')}")
    st.divider()

    progress = st.progress(0, text="Analysing contract — all sections running in parallel...")

    try:
        results = analyse_all(text)
        summary = results["summary"]
        clauses = results["clauses"]
        risks = results["risks"]
        questions = results["questions"]
        progress.progress(100, text="Analysis complete!")

    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate" in error_msg.lower():
            st.error("Rate limit hit. Please wait a moment and try again.")
        elif "api_key" in error_msg.lower() or "invalid" in error_msg.lower():
            st.error("Invalid or missing API key. Check your .env file.")
        else:
            st.error("Analysis failed. Please try again.")
            st.caption(f"Error detail: {e}")
        st.stop()

    st.session_state["summary"] = summary
    st.session_state["clauses"] = clauses
    st.session_state["risks"] = risks
    st.session_state["questions"] = questions
    st.session_state["contract_type"] = contract_type
    st.session_state["filename"] = uploaded_file.name


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Summary",
    "🔍 Key Clauses",
    "⚠️ Risk Flags",
    "❓ Questions to Ask",
    "💬 Chat with Contract"
])

with tab1:
    if "summary" in st.session_state:
        st.markdown(st.session_state["summary"])
    else:
        st.info("Upload and analyse a contract to see the summary.")

with tab2:
    if "clauses" in st.session_state:
        st.markdown(st.session_state["clauses"])
    else:
        st.info("Upload and analyse a contract to see key clauses.")

with tab3:
    if "risks" in st.session_state:
        st.warning(st.session_state["risks"])
    else:
        st.info("Upload and analyse a contract to see risk flags.")

with tab4:
    if "questions" in st.session_state:
        st.markdown(st.session_state["questions"])
    else:
        st.info("Upload and analyse a contract to see suggested questions.")

with tab5:
    st.markdown("### 💬 Chat with your Contract")
    st.markdown("Ask anything about the contract you uploaded.")

    if "contract_text" not in st.session_state:
        st.info("Upload and analyse a contract first to enable chat.")
    else:
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask a question about your contract...")

        if user_input:
            st.session_state["chat_history"].append({"role": "user", "content": user_input})

            with st.chat_message("user"):
                st.markdown(user_input)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        chat_prompt = f"""You are a legal expert assistant. The user has uploaded a contract and you have full access to it.
Answer their questions clearly and in plain English. Be specific and reference the actual contract text where relevant.

CONTRACT:
{st.session_state['contract_text']}

Question: {user_input}"""

                        message = client.messages.create(
                            model=MODEL,
                            max_tokens=1000,
                            messages=[{"role": "user", "content": chat_prompt}]
                        )
                        answer = message.content[0].text
                        st.markdown(answer)
                        st.session_state["chat_history"].append({"role": "assistant", "content": answer})

                    except Exception as e:
                        st.error(f"Chat error: {e}")


if "summary" in st.session_state:
    full_report = f"""AI LEGAL DOCUMENT ANALYSER — FULL REPORT

Document: {st.session_state['filename']}
Contract type: {st.session_state['contract_type']}
Analysed on: {datetime.now().strftime('%d %B %Y at %H:%M')}

DISCLAIMER: AI-generated analysis for informational purposes only. Not legal advice.

----------------------------------------
SUMMARY
----------------------------------------
{st.session_state['summary']}

----------------------------------------
KEY CLAUSES
----------------------------------------
{st.session_state['clauses']}

----------------------------------------
RISK FLAGS
----------------------------------------
{st.session_state['risks']}

----------------------------------------
QUESTIONS TO ASK BEFORE SIGNING
----------------------------------------
{st.session_state['questions']}

----------------------------------------
Generated by AI Legal Document Analyser · Powered by Claude AI
"""

    st.divider()
    st.download_button(
        label="📥 Download Full Report",
        data=full_report,
        file_name=f"analysis_{st.session_state['filename'].replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )
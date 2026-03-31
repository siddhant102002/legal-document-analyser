# AI Legal Document Analyser

An AI-powered tool that helps users understand legal contracts by providing a clear summary, key clauses, risk analysis, and important questions before signing.

## Demo

Demo video will be added here.

---

## Features

- ✅ **Handles any file size** - Intelligent chunking for large documents (100K+ characters)
- ✅ **Free AI** - Uses Gemini 1.5 Flash (no cost, generous limits)
- ✅ **Identifies key clauses** - termination, confidentiality, liability, obligations, etc.
- ✅ **Plain English summaries** - Easy to understand for non-lawyers
- ✅ **Risk analysis** - Highlights one-sided terms, unfair clauses, missing protections
- ✅ **Smart questions** - Important questions to ask before signing
- ✅ **PDF & Word support** - Upload contracts in either format
- ✅ **Download report** - Full analysis saved as text file
- ✅ **Robust** - Automatic retry for rate limits, clear error messages

---

## Technologies

- **Google Gemini 1.5 Flash** (Free API)
- Python  
- Streamlit  
- pypdf  
- python-docx  

---

## How It Works

The application follows a simple 4-step process:

1. **Upload**  
   The user uploads a contract in PDF or Word format  

2. **Extract**  
   The system extracts all text from the document using document parsing libraries  

3. **Analyse**  
   The extracted text is sent to **Gemini 1.5 Flash** (free), which performs:
   - Contract summarisation  
   - Clause identification  
   - Risk analysis  
   - Question generation  

   **Large document support**: Documents larger than 100K characters are automatically split into overlapping chunks for comprehensive analysis. The AI intelligently combines results from all chunks.

4. **Report**  
   Results are displayed in a structured format across multiple tabs, with an option to download the full report  

**Flow**: Upload → Extract → Analyse → Report  

---

## Setup Instructions

Follow these steps to run the project locally:

### 1. Get a Free Gemini API Key

- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Sign in with your Google account
- Click **Get API Key** → **Create API Key**
- This is **completely free** with generous rate limits

### 2. Clone and Install

```bash
git clone https://github.com/siddhant102002/legal-document-analyser.git
cd legal-document-analyser
pip install -r requirements.txt
```

### 3. Configure API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**Important**: Never commit your `.env` file. It's already in `.gitignore`.

### 4. Run the Application

```bash
streamlit run app.py
# or
python -m streamlit run app.py
```

Open the browser link shown in the terminal (usually http://localhost:8501)

---

## Use Cases

This tool can be used by:

- Freelancers reviewing client contracts before signing  
- Small businesses without access to legal teams  
- Individuals reviewing rental or lease agreements  
- Students learning about legal documents  
- Anyone who wants a quick understanding of complex contracts  

---

## Disclaimer

This tool provides AI-powered analysis for informational purposes only.

It is not a substitute for professional legal advice. Always consult a qualified legal professional before making decisions based on any contract.
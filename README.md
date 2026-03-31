# AI Legal Document Analyser

An AI-powered tool that helps users understand legal contracts by providing a clear summary, key clauses, risk analysis, and important questions before signing.

## Demo

Demo video will be added here.

---

## Features

- Identifies key clauses such as termination, confidentiality, liability, and obligations  
- Summarises contracts in plain, easy-to-understand language  
- Highlights potential risks, one-sided terms, and missing protections  
- Suggests important questions to ask before signing  
- Supports both PDF and Word document uploads  

---

## Technologies

- Google Gemini API  
- Python  
- Streamlit  
- pypdf  
- python-docx  

---

## How It Works

The application follows a simple 4-step process:

1. Upload  
   The user uploads a contract in PDF or Word format  

2. Extract  
   The system extracts all text from the document using document parsing libraries  

3. Analyse  
   The extracted text is sent to an AI model (Gemini API), which performs:
   - Contract summarisation  
   - Clause identification  
   - Risk analysis  
   - Question generation  

4. Report  
   Results are displayed in a structured format across multiple tabs, with an option to download the full report  

Flow:

Upload → Extract → Analyse → Report  

---

## Setup Instructions

Follow these steps to run the project locally:

1. Clone the repository  
   git clone https://github.com/siddhant102002/legal-document-analyser.git  
   cd legal-document-analyser  

2. Install dependencies  
   pip install -r requirements.txt  

3. Create a `.env` file in the root directory and add your API key  
   GEMINI_API_KEY=your_api_key_here  

4. Run the application  
   python -m streamlit run app.py  

5. Open the browser link shown in the terminal  

The app should now be running locally  

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
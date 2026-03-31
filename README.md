# ⚖️ AI Legal Document Analyser

An AI-powered legal document analysis tool built with Streamlit and Claude AI. Upload any contract and get an instant, plain-English breakdown — no legal background needed.

## 🔍 Features

- **Contract Summary** — plain English overview of what the contract says
- **Key Clauses** — all important clauses identified and explained
- **Risk Flags** — one-sided or unfair clauses highlighted
- **Questions to Ask** — 8 smart questions to ask before signing
- **Chat with Contract** — ask anything about your document in real time
- **Download Report** — full analysis exported as a text file

## 🛠 Tech Stack

- Python
- Streamlit
- Anthropic Claude API (claude-sonnet-4-5)
- PyPDF2 / python-docx for document parsing
- Concurrent processing for fast parallel analysis

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/siddhant102002/legal-document-analyser.git
cd legal-document-analyser
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from [console.anthropic.com](https://console.anthropic.com)

### 4. Run the app
```bash
streamlit run app.py
```

## 📁 Project Structure
```
legal-document-analyser/
├── app.py                  # Main Streamlit app
├── analyser.py             # Claude AI analysis functions
├── document_reader.py      # PDF and DOCX text extraction
├── requirements.txt        # Dependencies
├── .env                    # API key (not committed)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## ⚠️ Disclaimer

This tool provides AI-generated analysis for informational purposes only. It is not legal advice. Always consult a qualified solicitor before signing any contract.

## 👨‍💻 Built by

Siddhant Tayade — [LinkedIn](https://linkedin.com/in/siddhant-tayade-1b92a2396) · [GitHub](https://github.com/siddhant102002)

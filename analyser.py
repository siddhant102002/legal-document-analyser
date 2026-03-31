import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-latest")


# 🔹 1. Summary
def summarise_contract(contract_text):
    prompt = f"""
You are a legal expert. Read this contract and write a clear summary in plain English for someone with no legal background.

Cover:
- what this contract is about
- who the parties are
- what each party must do
- how long it lasts
- how it ends

Contract:
{contract_text}
"""
    response = model.generate_content(prompt)
    return response.text


# 🔹 2. Key Clauses
def identify_clauses(contract_text):
    prompt = f"""
You are a legal expert. Identify ALL key clauses in this contract.

For each clause return:
- Clause Name
- What It Says (in plain English)
- Why It Matters

Look for:
payment terms, termination, liability, confidentiality, intellectual property, dispute resolution, governing law.

Contract:
{contract_text}
"""
    response = model.generate_content(prompt)
    return response.text


# 🔹 3. Risk Flags
def flag_risks(contract_text):
    prompt = f"""
You are a legal expert reviewing this contract for risks.

Identify any clauses that are:
- unusually one-sided
- potentially unfair
- legally risky
- missing protections
- unusual

For each risk:
- what it says
- why it is risky
- what a fairer version would look like

Contract:
{contract_text}
"""
    response = model.generate_content(prompt)
    return response.text


# 🔹 4. Questions
def suggest_questions(contract_text):
    prompt = f"""
Based on this contract, list the 8 most important questions someone should ask before signing it.

Focus on:
- unclear terms
- missing details
- potential problems

Contract:
{contract_text}
"""
    response = model.generate_content(prompt)
    return response.text
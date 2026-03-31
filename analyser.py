import google.generativeai as genai
from dotenv import load_dotenv
import os
import time
import random

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def call_gemini_with_retry(prompt, max_retries=3):
    """Call Gemini API with exponential backoff retry for rate limits."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    continue
            raise e
    raise Exception(f"Failed after {max_retries} attempts")


def chunk_text(text, chunk_size=50000, overlap=2000):
    """
    Split large text into overlapping chunks for processing.
    Tries to split at paragraph boundaries.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to find a good break point (paragraph or sentence)
        if end < len(text):
            # Look for paragraph break
            paragraph_break = text.rfind('\n\n', start, end)
            if paragraph_break > start + chunk_size // 2:
                end = paragraph_break
            else:
                # Look for sentence break (period followed by space)
                sentence_break = text.rfind('. ', start, end)
                if sentence_break > start + chunk_size // 2:
                    end = sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start forward, accounting for overlap
        start = end - overlap if end < len(text) else len(text)

    return chunks


# 🔹 1. Summary
def summarise_contract(contract_text):
    chunks = chunk_text(contract_text, chunk_size=50000)

    if len(chunks) == 1:
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
        return call_gemini_with_retry(prompt)

    # For multiple chunks, get summaries and combine
    summaries = []
    for i, chunk in enumerate(chunks[:3]):  # Limit to first 3 chunks to avoid excessive API calls
        prompt = f"""
You are a legal expert. Read this part of a contract (part {i+1}) and extract key information.

Focus on:
- Parties involved
- Key obligations
- Important dates/duration
- Special terms

Contract section:
{chunk}
"""
        summary = call_gemini_with_retry(prompt)
        summaries.append(f"Part {i+1} summary:\n{summary}")

    # Combine summaries
    combined_prompt = f"""
Based on these partial summaries of a contract, create a single coherent summary covering:
- What the contract is about
- Who the parties are
- What each party must do
- How long it lasts
- How it ends

Summaries:
{' '.join(summaries)}
"""
    return call_gemini_with_retry(combined_prompt)


# 🔹 2. Key Clauses
def identify_clauses(contract_text):
    chunks = chunk_text(contract_text, chunk_size=50000)

    if len(chunks) == 1:
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
        return call_gemini_with_retry(prompt)

    # For multiple chunks, get clauses from each and combine
    all_clauses = []
    for chunk in chunks[:3]:  # Limit to first 3 chunks
        prompt = f"""
You are a legal expert. Identify key clauses in this contract section.

For each clause return:
- Clause Name
- What It Says (in plain English)
- Why It Matters

Contract section:
{chunk}
"""
        clause_text = call_gemini_with_retry(prompt)
        all_clauses.append(clause_text)

    # Ask AI to deduplicate and combine
    combined_prompt = f"""
Combine these clause lists from different sections of the same contract.
Remove duplicates and organize into a single coherent list.

Sections:
{' '.join(all_clauses)}
"""
    return call_gemini_with_retry(combined_prompt)


# 🔹 3. Risk Flags
def flag_risks(contract_text):
    chunks = chunk_text(contract_text, chunk_size=50000)

    if len(chunks) == 1:
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
        return call_gemini_with_retry(prompt)

    # For multiple chunks, get risks from each and combine
    all_risks = []
    for chunk in chunks[:3]:  # Limit to first 3 chunks
        prompt = f"""
You are a legal expert reviewing this contract section for risks.

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

Contract section:
{chunk}
"""
        risk_text = call_gemini_with_retry(prompt)
        all_risks.append(risk_text)

    # Combine risk assessments
    combined_prompt = f"""
Combine these risk assessments from different sections of the same contract.
Remove duplicates and prioritize the most critical risks.

Risk assessments:
{' '.join(all_risks)}
"""
    return call_gemini_with_retry(combined_prompt)


# 🔹 4. Questions
def suggest_questions(contract_text):
    chunks = chunk_text(contract_text, chunk_size=50000)

    if len(chunks) == 1:
        prompt = f"""
Based on this contract, list the 8 most important questions someone should ask before signing it.

Focus on:
- unclear terms
- missing details
- potential problems

Contract:
{contract_text}
"""
        return call_gemini_with_retry(prompt)

    # For multiple chunks, get questions from each and combine
    all_questions = []
    for chunk in chunks[:2]:  # Limit to first 2 chunks
        prompt = f"""
Based on this contract section, list the 5 most important questions someone should ask before signing.

Focus on:
- unclear terms
- missing details
- potential problems

Contract section:
{chunk}
"""
        questions_text = call_gemini_with_retry(prompt)
        all_questions.append(questions_text)

    # Combine and prioritize questions
    combined_prompt = f"""
Combine these question lists from different sections of the same contract.
Remove duplicates and select the 8 most important overall questions.

Questions from sections:
{' '.join(all_questions)}
"""
    return call_gemini_with_retry(combined_prompt)
import anthropic
from dotenv import load_dotenv
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def call_claude(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model=MODEL,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            if "429" in str(e) or "rate" in str(e).lower():
                if attempt < max_retries - 1:
                    time.sleep((2 ** attempt) + random.uniform(0, 1))
                    continue
            raise e
    raise Exception("Failed after retries")


def detect_contract_type(text):
    try:
        return call_claude(f"What type of contract is this? Reply with ONLY the contract type name. Examples: Non-Disclosure Agreement, Employment Contract, Service Agreement.\n\n{text[:1000]}")
    except Exception:
        return "Legal Contract"


def summarise_contract(text):
    return call_claude(f"""You are a legal expert. Read this entire contract and write a clear summary in plain English for someone with no legal background.

Cover:
- What this contract is about
- Who the parties are
- What each party must do
- How long it lasts
- How it ends

Contract:
{text}""")


def identify_clauses(text):
    return call_claude(f"""You are a legal expert. Identify ALL key clauses in this contract.

For each clause:
- Clause Name
- What It Says (plain English)
- Why It Matters

Look for: payment terms, termination, liability, confidentiality, intellectual property, dispute resolution, governing law.

Contract:
{text}""")


def flag_risks(text):
    return call_claude(f"""You are a legal expert reviewing this contract for risks.

Identify clauses that are:
- Unusually one-sided
- Potentially unfair
- Legally risky
- Missing important protections

For each risk:
- What it says
- Why it is risky
- What a fairer version would look like

Contract:
{text}""")


def suggest_questions(text):
    return call_claude(f"""Based on this contract, list the 8 most important questions someone should ask before signing.

Focus on:
- Unclear terms
- Missing details
- Potential problems

Contract:
{text}""")


def analyse_all(text):
    results = {}
    tasks = {
        "summary": summarise_contract,
        "clauses": identify_clauses,
        "risks": flag_risks,
        "questions": suggest_questions,
    }
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fn, text): key for key, fn in tasks.items()}
        for future in as_completed(futures):
            key = futures[future]
            results[key] = future.result()
    return results
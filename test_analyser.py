from document_reader import extract_text
from analyser import (
    summarise_contract,
    identify_clauses,
    flag_risks,
    suggest_questions
)

# Load contract
text = extract_text("sample_contract.pdf")

# Clean text
text = " ".join(text.split())

print("\n🔹 SUMMARY\n")
print(summarise_contract(text))

print("\n🔹 KEY CLAUSES\n")
print(identify_clauses(text))

print("\n🔹 RISKS\n")
print(flag_risks(text))

print("\n🔹 QUESTIONS\n")
print(suggest_questions(text))
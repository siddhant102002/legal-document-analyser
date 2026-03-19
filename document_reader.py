from pypdf import PdfReader
from docx import Document


def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "

    return text.strip()


def read_docx(file_path):
    doc = Document(file_path)
    text = " ".join([p.text for p in doc.paragraphs])
    return text.strip()


def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return read_pdf(file_path)
    elif file_path.endswith('.docx'):
        return read_docx(file_path)
    else:
        raise ValueError("Only PDF and DOCX supported")


# 🔽 Test it
if __name__ == "__main__":
    text = extract_text("sample_contract.pdf")

    # Clean text
    text = " ".join(text.split())

    print(text[:500])
    print(f"\nExtracted {len(text)} characters from document")

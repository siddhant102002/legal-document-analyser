from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "What are the 5 most important clauses in a standard employment contract? Explain each in plain English."
        }
    ],
    model="llama-3.1-8b-instant"
)

print(chat_completion.choices[0].message.content)
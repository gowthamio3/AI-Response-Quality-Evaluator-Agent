import os
from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
model="gemini-3.1-flash-lite",
    contents="Say hello in one sentence"
)

print(response.text)
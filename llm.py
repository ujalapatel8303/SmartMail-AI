import os

from dotenv import load_dotenv
from google import genai

from prompts import SYSTEM_PROMPT


# Load variables from .env
load_dotenv()


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check if API key exists
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file"
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_email(email_text):

    prompt = f"""
{SYSTEM_PROMPT}

Here is the email:

{email_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
def generate_smart_reply(email_text, tone="Professional"):

    prompt = f"""
You are SmartMail AI.

Generate a smart email reply to the following email.

Reply tone: {tone}

Requirements:
- Be polite and natural.
- Directly respond to the email.
- Keep the reply concise.
- Do not invent information.
- Do not include a subject line.
- Return only the reply text.

Email:
{email_text}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text
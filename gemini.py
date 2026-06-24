import os
from dotenv import load_dotenv
from google import genai
from prompts import support_triage_prompt

load_dotenv()

def triage_support_request(issue: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "Category: Test\n"
            "Priority: Medium\n"
            "Reason: Gemini API key is not set yet.\n"
            "Missing info: Add GEMINI_API_KEY to .env.\n"
            "Draft reply: Thanks for reaching out. We are setting up SupportOps AI and will respond shortly."
        )

    client = genai.Client(api_key=api_key)

    prompt = support_triage_prompt(issue)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
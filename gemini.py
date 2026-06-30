import os
from dotenv import load_dotenv
import google.generativeai as genai

from prompts import SUPPORT_ANALYSIS_PROMPT, SUPPORT_SUMMARY_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def fallback_analysis(user_text: str) -> str:
    text = user_text.lower()

    if any(word in text for word in ["down", "outage", "cannot access", "can't access", "urgent"]):
        priority = "High"
    elif any(word in text for word in ["can't log in", "cannot log in", "login", "password"]):
        priority = "Medium"
    else:
        priority = "Low"

    return f"""*Issue type:* Account / Access Support
*Priority:* {priority}
*Summary:* The user is having trouble with: "{user_text}"

*Suggested draft reply:*
Hi, thanks for reaching out. I understand you're having trouble with this. I’ll help look into it now. Please confirm your username/email and whether you are seeing any error message.

*Recommended next action:*
Check the user's account status, recent login attempts, password reset status, and any related system alerts."""


def analyze_support_request(user_text: str) -> str:
    prompt = SUPPORT_TRIAGE_PROMPT + user_text

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return fallback_analysis(user_text)

def analyze_support_summary(tickets: str) -> str:
    prompt = SUPPORT_SUMMARY_PROMPT.format(tickets=tickets)
    response = model.generate_content(prompt)

    return response.text.strip()



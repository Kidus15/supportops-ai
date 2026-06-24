import os
from dotenv import load_dotenv
from slack_bolt import App
from gemini import triage_support_request

load_dotenv()

slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET")

if not slack_bot_token or not slack_signing_secret:
    raise ValueError("Missing Slack credentials. Add SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET to .env")

app = App(
    token=slack_bot_token,
    signing_secret=slack_signing_secret
)

@app.command("/support")
def handle_support_command(ack, command, respond):
    ack()

    issue = command.get("text", "").strip()

    if not issue:
        respond("Please describe the support issue after `/support`.")
        return

    try:
        result = triage_support_request(issue)

        respond({
            "response_type": "in_channel",
            "text": f"*SupportOps AI triage result*\n\n{result}"
        })

    except Exception as e:
        print("Error:", e)
        respond({
            "response_type": "ephemeral",
            "text": "Something went wrong while triaging the request. Please try again."
        })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.start(port=port)
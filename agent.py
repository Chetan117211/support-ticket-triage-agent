import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from models import Ticket, TriageResult


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to your .env file."
    )

client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
You are an AI Support Ticket Triage Agent.

Your job is to analyze customer support tickets and classify them.

Allowed categories:
- Billing
- Technical
- Account
- Delivery
- Refund
- Product
- Security
- Other

Allowed urgency levels:
- Low
- Medium
- High
- Critical

Rules:

1. Choose the category that best represents the customer's main issue.
2. Choose urgency based on impact and time sensitivity.
3. Critical issues include serious security incidents, major service outages,
   or situations requiring immediate intervention.
4. High urgency includes significant payment problems, account access issues,
   or important service failures.
5. Medium represents normal issues requiring attention.
6. Low represents informational or minor requests.
7. Give a confidence score between 0 and 1.
8. Do not pretend certainty when the ticket is ambiguous.
9. Give a short explanation for your decision.
"""


def classify_ticket(ticket: Ticket) -> TriageResult:

    prompt = f"""
{SYSTEM_PROMPT}

Analyze this support ticket:

Ticket ID: {ticket.ticket_id}

Subject:
{ticket.subject}

Body:
{ticket.body}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TriageResult,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return TriageResult.model_validate_json(response.text)
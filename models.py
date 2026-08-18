from typing import Literal
from pydantic import BaseModel, Field


Category = Literal[
    "Billing",
    "Technical",
    "Account",
    "Delivery",
    "Refund",
    "Product",
    "Security",
    "Other",
]

Urgency = Literal[
    "Low",
    "Medium",
    "High",
    "Critical",
]


class Ticket(BaseModel):
    ticket_id: str
    subject: str
    body: str


class TriageResult(BaseModel):
    ticket_id: str
    category: Category
    urgency: Urgency
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
from models import TriageResult


ROUTING_MAP = {
    "Billing": "Billing Team",
    "Technical": "Technical Support",
    "Account": "Account Team",
    "Delivery": "Delivery Team",
    "Refund": "Billing Team",
    "Product": "Product Team",
    "Security": "Security Team",
    "Other": "Human Review",
}


HUMAN_REVIEW_THRESHOLD = 0.65


def apply_routing(result: TriageResult) -> dict:
    """
    Apply deterministic routing and human-review rules.
    """

    human_review = result.confidence < HUMAN_REVIEW_THRESHOLD

    if human_review:
        routing_team = "Human Review"
    else:
        routing_team = ROUTING_MAP[result.category]

    return {
        "ticket_id": result.ticket_id,
        "category": result.category,
        "urgency": result.urgency,
        "confidence": result.confidence,
        "routing_team": routing_team,
        "human_review": human_review,
        "reason": result.reason,
    }
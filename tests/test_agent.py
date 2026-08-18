from models import TriageResult
from routing import apply_routing


def test_high_confidence_ticket_routes_correctly():
    result = TriageResult(
        ticket_id="TEST001",
        category="Billing",
        urgency="High",
        confidence=0.95,
        reason="Payment issue.",
    )

    output = apply_routing(result)

    assert output["routing_team"] == "Billing Team"
    assert output["human_review"] is False


def test_low_confidence_ticket_goes_to_human_review():
    result = TriageResult(
        ticket_id="TEST002",
        category="Technical",
        urgency="Medium",
        confidence=0.40,
        reason="Ambiguous issue.",
    )

    output = apply_routing(result)

    assert output["routing_team"] == "Human Review"
    assert output["human_review"] is True


def test_confidence_must_be_between_zero_and_one():
    try:
        TriageResult(
            ticket_id="TEST003",
            category="Billing",
            urgency="High",
            confidence=1.5,
            reason="Invalid confidence.",
        )

        assert False, "Invalid confidence should have been rejected"

    except ValueError:
        assert True
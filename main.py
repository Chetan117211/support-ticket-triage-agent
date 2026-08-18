from models import Ticket
from agent import classify_ticket
from routing import apply_routing


def main():
    ticket = Ticket(
        ticket_id="T001",
        subject="Payment deducted but order failed",
        body=(
            "I placed an order yesterday. The amount was deducted "
            "from my bank account but the order still shows as failed."
        ),
    )

    # Step 1: Ask Gemini to classify the ticket
    result = classify_ticket(ticket)

    # Step 2: Apply routing and human-review rules
    final_result = apply_routing(result)

    print("\n===== SUPPORT TICKET TRIAGE =====")

    for key, value in final_result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
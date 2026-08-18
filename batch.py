import json

from models import Ticket
from agent import classify_ticket
from routing import apply_routing


def load_tickets(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Ticket.model_validate(ticket) for ticket in data]


def process_batch(tickets):
    results = []

    for ticket in tickets:
        print(f"Processing {ticket.ticket_id}...")

        try:
            classification = classify_ticket(ticket)
            result = apply_routing(classification)
            results.append(result)

        except Exception as error:
            print(f"Error processing {ticket.ticket_id}: {error}")

            results.append({
                "ticket_id": ticket.ticket_id,
                "category": "Other",
                "urgency": "Medium",
                "confidence": 0.0,
                "routing_team": "Human Review",
                "human_review": True,
                "reason": f"Processing failed: {error}",
            })

    return results


def save_results(results, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


def main():
    tickets = load_tickets("data/sample_tickets.json")

    results = process_batch(tickets)

    save_results(results, "data/output.json")

    print("\n===== BATCH COMPLETE =====")
    print(f"Processed tickets: {len(results)}")
    print("Output saved to: data/output.json")


if __name__ == "__main__":
    main()
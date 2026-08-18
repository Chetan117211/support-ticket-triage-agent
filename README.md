# Support Ticket Triage Agent

A lightweight Python agent that classifies and routes customer support tickets. It uses a language model for semantic classification and deterministic Python rules for routing and human-review decisions.

Key goals: accuracy, explainability, and simple reproducibility.

---

## Quick Summary

- Input: ticket JSON with `ticket_id`, `subject`, and `body`.
- Output: `category`, `urgency`, `confidence` (0.0–1.0), `routing_team`, `human_review` (bool), and `reason`.
- Deterministic routing is implemented in `routing.py`; the LLM only provides classification and a confidence estimate.

---

## Features

- Natural-language classification using an LLM
- Urgency detection
- Confidence score and human-review gating
- Deterministic routing rules
- Batch processing with structured JSON output
- Pydantic validation for model outputs
- Error handling for failed ticket processing
- Automated tests for routing and human-review logic
- CLI-based execution

---

## Architecture

```text
                    Support Ticket

                         |
                         v

                 +-------------------+
                 |    Gemini LLM     |
                 | Semantic Analysis |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Pydantic Schema   |
                 |    Validation     |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Deterministic     |
                 | Routing Logic     |
                 +---------+---------+
                           |
                    +------+------+
                    |             |
                    v             v
               Team Route    Human Review
                    |
                    v
               Structured JSON
```

### Batch Workflow

```text
15 Support Tickets
        |
        v
    Batch Processor
        |
        +--> Gemini Classification
        |
        +--> Pydantic Validation
        |
        +--> Routing
        |
        +--> Human Review Check
        |
        v
    data/output.json
```

---

## Technology Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Application development         |
| Google Gemini API | AI-based ticket classification  |
| Pydantic          | Structured data validation      |
| python-dotenv     | Environment variable management |
| pytest            | Automated testing               |
| JSON              | Input and output data           |

---

## Project Layout

```text
support-ticket-triage-agent/
├── agent.py           # LLM integration and per-ticket processing
├── batch.py           # Batch runner
├── main.py            # Example single-ticket runner
├── models.py          # Pydantic models for input/output
├── routing.py         # Deterministic routing rules
├── data/
│   ├── sample_tickets.json
│   └── output.json
├── tests/
│   └── test_agent.py
├── requirements.txt
├── .gitignore
└── README.md
```

> Note: `.env` and virtual-environment directories are local-only files and should not be committed to GitHub.

---

## Ticket Categories

The agent supports the following categories:

- Billing
- Technical
- Account
- Delivery
- Refund
- Product
- Security
- Other

---

## Urgency Levels

The agent supports four urgency levels:

- Low
- Medium
- High
- Critical

The urgency is determined by the potential impact and time sensitivity of the customer's issue.

### Low

General product information or routine account changes.

### Medium

Normal delivery, performance, refund, or support issues.

### High

Significant payment problems, account access problems, or important service failures.

### Critical

Serious security incidents or situations requiring immediate intervention.

---

## Routing Logic

Routing is deliberately handled using deterministic Python rules rather than asking the LLM to decide the team.

| Category  | Routing Team      |
| --------- | ----------------- |
| Billing   | Billing Team      |
| Refund    | Billing Team      |
| Technical | Technical Support |
| Account   | Account Team      |
| Delivery  | Delivery Team     |
| Product   | Product Team      |
| Security  | Security Team     |
| Other     | Human Review      |

This separation makes the routing behavior predictable and easier to test.

---

## Confidence and Human Review

The AI returns a confidence score between `0.0` and `1.0`.

The application uses the following decision boundary:

```text
confidence < 0.65
        |
        v
Human Review = True
Routing Team = Human Review
```

Tickets with confidence of `0.65` or higher are routed according to their category.

For example:

```json
{
  "ticket_id": "T014",
  "category": "Technical",
  "urgency": "Low",
  "confidence": 0.3,
  "routing_team": "Human Review",
  "human_review": true,
  "reason": "The ticket is extremely vague and provides insufficient information."
}
```

The confidence value should be interpreted as an application-level estimate from the language model rather than a statistically calibrated probability.

The human-review mechanism prevents the system from automatically routing tickets when the available information is too ambiguous.

---

## Input Format

A ticket uses the following structure:

```json
{
  "ticket_id": "T001",
  "subject": "Payment deducted but order failed",
  "body": "I was charged but my order did not complete."
}
```

---

## Output Format

The agent produces structured output such as:

```json
{
  "ticket_id": "T001",
  "category": "Billing",
  "urgency": "High",
  "confidence": 0.95,
  "routing_team": "Billing Team",
  "human_review": false,
  "reason": "The customer was charged money for an order that failed."
}
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Chetan117211/support-ticket-triage-agent.git
cd support-ticket-triage-agent
```

### Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

If PowerShell activation is restricted, the project can also be run directly using:

```powershell
.\venv\Scripts\python.exe
```

### Install Dependencies

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

The API key must not be committed to GitHub.

The `.gitignore` file excludes `.env`.

---

## Run a Single Ticket

Run:

```powershell
.\venv\Scripts\python.exe main.py
```

The program sends a sample support ticket to Gemini and then applies the deterministic routing and human-review logic.

Example:

```text
===== SUPPORT TICKET TRIAGE =====

ticket_id: T001
category: Billing
urgency: High
confidence: 0.95
routing_team: Billing Team
human_review: False
reason: The customer was charged money for an order that failed...
```

---

## Run Batch Processing

Sample tickets are stored in:

```text
data/sample_tickets.json
```

The project contains 15 sample support tickets covering different categories, urgency levels, and an intentionally ambiguous case.

Run:

```powershell
.\venv\Scripts\python.exe batch.py
```

The processed results are written to:

```text
data/output.json
```

Example:

```text
Processing T001...
Processing T002...
Processing T003...
...
Processing T015...

===== BATCH COMPLETE =====

Processed tickets: 15
Output saved to: data/output.json
```

---

## Testing

The project includes automated tests for the deterministic logic.

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
```

The tests verify:

- Correct routing for high-confidence tickets
- Human-review behavior for low-confidence tickets
- Confidence validation

### Test Result

```text
3 passed
```

The tests do not require additional Gemini API calls.

---

## Design Decisions

### Why Use an LLM?

Support tickets are written in natural language and can describe the same problem using many different words.

An LLM is useful for understanding the semantic meaning of the ticket and mapping it to a controlled category and urgency level.

### Why Use Google Gemini?

Google Gemini was selected because it provides natural-language understanding suitable for support-ticket classification and supports structured JSON output that integrates with Pydantic validation.

The available Gemini API access also allowed the project to be developed and tested within the time constraints of the challenge.

### Why Use Pydantic?

The LLM output is validated using Pydantic before being passed to the routing layer.

This prevents malformed or invalid values from silently entering the application.

### Why Deterministic Routing?

The LLM identifies the customer's issue, but routing is handled by Python rules.

This makes routing predictable, testable, and easy to modify without changing the AI prompt.

### Why Human Review?

An AI system should not make uncertain routing decisions automatically.

Tickets below the confidence threshold are therefore routed to human review.

### Why CLI Instead of a UI?

The assessment evaluates a working agent and allows a command-line application.

Development time was prioritized toward the core agent, batch processing, validation, testing, and reproducibility rather than building a user interface.

---

## Tradeoffs

### LLM Confidence

The confidence value is an application-level estimate generated by the model and is not statistically calibrated.

A production system could improve this by evaluating the classifier against a labeled dataset and calibrating confidence thresholds.

### Taxonomy

The project uses a deliberately small category set.

A production implementation could support organization-specific categories and hierarchical ticket classifications.

### Batch Processing

The current batch processor processes tickets sequentially.

A production implementation could use asynchronous processing while respecting API rate limits.

### Human Review

The current implementation uses a fixed confidence threshold of `0.65`.

A production system could determine this threshold using historical support-ticket data and business risk requirements.

---

## Limitations

- Classification quality depends on the underlying language model.
- Confidence scores are not calibrated probabilities.
- The project uses a fixed ticket taxonomy.
- Routing rules are currently configured in Python.
- Batch processing is sequential.
- The project does not maintain historical ticket state.
- No production database is included.

---

## Future Improvements

With additional development time, the system could be extended with:

- Streamlit web interface
- Persistent ticket database
- Historical ticket analytics
- Organization-specific routing rules
- Confidence calibration
- Asynchronous batch processing
- Authentication
- Monitoring and logging
- Human feedback collection
- Evaluation against a labeled benchmark dataset

---

## Sample Result

The sample batch contains 15 tickets.

Examples include:

- Billing problems
- Account access issues
- Technical failures
- Delivery delays
- Refund requests
- Product questions
- Security incidents
- Ambiguous tickets

The ambiguous ticket demonstrates the human-review mechanism:

```text
Confidence: 0.30
Routing: Human Review
Human Review: True
```

This demonstrates the agent's ability to avoid making an automatic decision when the input is insufficiently specific.

The complete classified batch output is available in:

```text
data/output.json
```

---

## Assessment Requirements

| Requirement                          | Implementation               |
| ------------------------------------ | ---------------------------- |
| Accept support ticket subject + body | `Ticket` model               |
| Category classification              | Gemini                       |
| Urgency classification               | Gemini                       |
| Confidence score                     | Gemini + Pydantic validation |
| Team routing                         | Deterministic Python routing |
| Human review                         | Confidence threshold         |
| Batch processing                     | `batch.py`                   |
| Sample tickets                       | `data/sample_tickets.json`   |
| Classified output                    | `data/output.json`           |
| Decision boundary explanation        | README                       |
| Runnable agent                       | `main.py` / `batch.py`       |
| Tests                                | `tests/test_agent.py`        |
| Setup instructions                   | README                       |
| Tradeoff notes                       | README                       |

---

## Conclusion

The Support Ticket Triage Agent combines LLM-based natural-language understanding with deterministic business rules.

The resulting workflow is:

```text
Input Ticket
     ↓
Gemini Classification
     ↓
Pydantic Validation
     ↓
Confidence Check
     ↓
Routing Decision
     ↓
Human Review if Uncertain
     ↓
Structured Output
```

The design prioritizes reliability, explainability, reproducibility, and a working end-to-end workflow within the constraints of the 24-hour challenge.

---

## GitHub Repository

[https://github.com/Chetan117211/support-ticket-triage-agent](https://github.com/Chetan117211/support-ticket-triage-agent)

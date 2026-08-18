# Support Ticket Triage Agent

An AI-powered support ticket triage agent built for the Rooman Technologies 24-Hour AI Agent Challenge.

The agent analyzes incoming customer support tickets, classifies them by category and urgency, estimates confidence, routes them to the appropriate support team, and sends uncertain cases to human review.

---

## 1. Problem Statement

Support teams receive large numbers of customer tickets that need to be categorized and routed efficiently.

This project automates the initial triage process using an AI language model while keeping routing and human-review decisions deterministic and explainable.

The agent accepts a ticket containing:

- Ticket ID
- Subject
- Body

It produces:

- Category
- Urgency
- Confidence score
- Routing team
- Human-review decision
- Reason for the classification

---

## 2. Features

- AI-based support ticket classification
- Category detection
- Urgency detection
- Confidence estimation
- Deterministic team routing
- Human-in-the-loop handling for uncertain tickets
- Batch processing of multiple tickets
- Structured JSON output
- Pydantic validation
- Error handling for failed ticket processing
- Automated tests
- CLI-based execution
- No database or UI dependency

---

## 3. Architecture

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
                    +-----+-----+
                    |           |
                    v           v
               Team Route   Human Review
                    |
                    v
              Structured JSON
```

### Batch workflow

```text
15+ Support Tickets
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

## 4. Technology Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Application development         |
| Google Gemini API | AI-based ticket classification  |
| Pydantic          | Structured data validation      |
| python-dotenv     | Environment variable management |
| pytest            | Automated testing               |
| JSON              | Input and output data           |

---

## 5. Project Structure

```text
support-ticket-triage-agent/
│
├── data/
│   ├── sample_tickets.json
│   └── output.json
│
├── tests/
│   └── test_agent.py
│
├── venv/
│
├── .env
├── .gitignore
├── models.py
├── agent.py
├── routing.py
├── batch.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 6. Ticket Categories

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

## 7. Urgency Levels

The agent supports four urgency levels:

- Low
- Medium
- High
- Critical

The urgency is determined by the potential impact and time sensitivity of the customer's issue.

Examples:

### Low

General product information or routine account changes.

### Medium

Normal delivery, performance, refund, or support issues.

### High

Significant payment problems, account access problems, or important service failures.

### Critical

Serious security incidents or situations requiring immediate intervention.

---

## 8. Routing Logic

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

## 9. Confidence and Human Review

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
  "human_review": true
}
```

The confidence value should be interpreted as an application-level estimate from the language model rather than a statistically calibrated probability.

The human-review mechanism prevents the system from confidently routing tickets when the available information is too ambiguous.

---

## 10. Input Format

A ticket uses the following structure:

```json
{
  "ticket_id": "T001",
  "subject": "Payment deducted but order failed",
  "body": "The amount was deducted but my order failed."
}
```

---

## 11. Output Format

The agent produces structured output such as:

```json
{
  "ticket_id": "T001",
  "category": "Billing",
  "urgency": "High",
  "confidence": 0.95,
  "routing_team": "Billing Team",
  "human_review": false,
  "reason": "The customer was charged for an order that failed."
}
```

---

## 12. Installation

### Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd support-ticket-triage-agent
```

### Create a virtual environment

Windows:

```powershell
python -m venv venv
```

If PowerShell activation is restricted, the project can also be run directly using:

```powershell
.\venv\Scripts\python.exe
```

### Install dependencies

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 13. Environment Configuration

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

The API key must not be committed to GitHub.

The `.gitignore` file excludes `.env`.

---

## 14. Run a Single Ticket

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

## 15. Run Batch Processing

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

## 16. Testing

The project includes automated tests for the deterministic logic.

Run:

```powershell
.\venv\Scripts\python.exe -m pytest
```

The tests verify:

- Correct routing for high-confidence tickets
- Human-review behavior for low-confidence tickets
- Confidence validation

The tests do not require additional Gemini API calls.

---

## 17. Design Decisions

### Why use an LLM?

Support tickets are written in natural language and can describe the same problem using many different words.

An LLM is useful for understanding the semantic meaning of the ticket and mapping it to a controlled category and urgency level.

### Why use Pydantic?

The LLM output is validated using Pydantic before being passed to the routing layer.

This prevents malformed or invalid values from silently entering the application.

### Why deterministic routing?

The LLM identifies the customer's issue, but routing is handled by Python rules.

This makes routing predictable, testable, and easy to modify without changing the AI prompt.

### Why human review?

An AI system should not make uncertain routing decisions automatically.

Tickets below the confidence threshold are therefore routed to human review.

### Why CLI instead of a UI?

The assessment evaluates a working agent and explicitly allows a command-line application.

Development time was prioritized toward the core agent, batch processing, validation, testing, and reproducibility rather than building a user interface.

---

## 18. Tradeoffs

### LLM confidence

The confidence value is an application-level estimate generated by the model and is not statistically calibrated.

A production system could improve this by evaluating the classifier against a labeled dataset and calibrating confidence thresholds.

### Taxonomy

The project uses a deliberately small category set.

A production implementation could support organization-specific categories and hierarchical ticket classifications.

### Batch processing

The current batch processor processes tickets sequentially.

A production implementation could use asynchronous processing while respecting API rate limits.

### Human review

The current implementation uses a fixed confidence threshold of `0.65`.

A production system could determine this threshold using historical support-ticket data and business risk requirements.

---

## 19. Limitations

- Classification quality depends on the underlying language model.
- Confidence scores are not calibrated probabilities.
- The project uses a fixed ticket taxonomy.
- Routing rules are currently configured in Python.
- Batch processing is sequential.
- The project does not maintain historical ticket state.
- No production database is included.

---

## 20. Future Improvements

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

## 21. Sample Result

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

---

## 22. Assessment Requirements

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

## 23. Conclusion

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

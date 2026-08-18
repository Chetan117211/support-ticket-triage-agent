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

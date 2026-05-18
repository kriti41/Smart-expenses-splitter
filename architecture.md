# 🏗️ Architecture Overview — Smart Expense Splitter

## Tech Stack Choice

### Why Python Instead of Node.js?

Python was selected for the complete stack because:

- FastAPI provides high-performance REST APIs with automatic validation and OpenAPI documentation
- Python has a stronger ecosystem for AI, NLP, OCR, and LLM integration
- Ollama integration for local LLM execution is easier in Python
- Pydantic enables strict schema validation for AI-generated outputs
- Streamlit allowed rapid frontend prototyping without needing Node.js

This project prioritizes:
- AI integration
- rapid development
- backend reliability
- easy experimentation

over highly complex frontend rendering.

---

# Backend Architecture

## Framework

### FastAPI

Used for:
- REST API development
- request validation
- automatic Swagger docs
- structured routing

---

# Database

## SQLite + SQLAlchemy ORM

SQLite was used for simplicity and fast local setup.

SQLAlchemy ORM manages:
- models
- relationships
- schema generation

---

# Database Schema

## Users

Stores user information.

| Field | Type |
|---|---|
| id | String |
| name | String |
| email | String |

---

## Expenses

Stores expense metadata.

| Field | Type |
|---|---|
| id | Integer |
| description | String |
| amount_paise | Integer |
| payer_id | String |
| group_id | String |

---

## Expense Shares

Stores how much each participant owes.

| Field | Type |
|---|---|
| id | Integer |
| expense_id | ForeignKey |
| user_id | String |
| owed_paise | Integer |

---

# Money Handling

All monetary values are stored as integers (paise).

Example:

```text
₹24.00 → 2400 paise

This avoids floating-point precision errors.

Floating-point money storage was intentionally avoided.

API Endpoints
Expense APIs
Create Expense
POST /expenses/

Creates a new expense with:

description
payer
group
participant shares

Validation ensures:

total shares equal total amount
required fields exist
invalid payloads are rejected
Root Endpoint
GET /

Health-check endpoint.

AI Parsing Endpoint
POST /ai/parse-expense

Accepts natural-language expense text.

Example:

I paid 2400 for dinner with Aman and Priya

Returns structured JSON.

Frontend Architecture
Streamlit Frontend

The frontend is organized into tab-based sections:

Add Expense
AI Expense Parser
Balances
Settle Up
OCR Upload

Streamlit was chosen because:

no Node.js setup required
quick iteration
Python-native integration
easy API calls
Settle-Up Algorithm
Goal

Minimize the number of transactions needed to settle debts.

Approach

A greedy debt simplification algorithm is used.

Process
Compute net balance for every user
positive → user should receive money
negative → user owes money
Separate:
debtors
creditors
Match largest debtor with largest creditor
Transfer minimum possible amount
Repeat until balances become zero
Example

Initial balances:

Aman  = -500
Priya = +300
Rahul = +200

Result:

Aman → Priya : 300
Aman → Rahul : 200

This reduces unnecessary transactions.

AI Architecture
Local LLM Integration

Ollama + TinyLlama are used for local inference.

Advantages:

free
offline capable
privacy-friendly
no API costs
NLP Expense Parsing

Input:

I paid 2400 for dinner split between me Aman and Priya

Pipeline:

User input received
Prompt sent to local LLM
LLM generates JSON
JSON parsed
Pydantic validation applied
Invalid outputs rejected
AI Failure Handling

AI systems are unreliable by nature.

This project includes defensive validation:

Failure Cases Handled
malformed JSON
missing fields
wrong datatypes
hallucinated structures
invalid schemas
Fallback Strategy

If AI parsing fails:

request is rejected safely
frontend can fallback to manual expense form
no invalid expense is saved automatically

This prevents hallucinated financial data from entering the database.

OCR Bill Upload

Current implementation:

UI upload support
image preview

Future improvement:

OCR text extraction
automatic line-item parsing
participant assignment

Potential tools:

Tesseract OCR
PaddleOCR
vision-capable LLMs

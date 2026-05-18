# Smart-expenses-splitter

# 💸 Smart Expense Splitter

An AI-powered expense splitting application inspired by Splitwise.

Users can:
- Create and manage shared expenses
- Split bills among friends
- Minimize settlement transactions
- Parse expenses using natural language
- Upload bill images for OCR parsing

Built using:
- FastAPI
- Streamlit
- SQLAlchemy
- Ollama (Local LLM)
- SQLite

---

# Features

## Core Features

### Group Expense Management
- Add shared expenses
- Store payer, amount, group, participants
- Equal split support
- Integer money handling (paise)

### REST API
- FastAPI backend
- Swagger/OpenAPI docs
- Validation using Pydantic

### Settle-Up Algorithm
- Minimizes number of transactions
- Debt simplification logic implemented

### Expense Validation
- Split amounts validated server-side
- Prevents invalid totals

---

# AI Features

## Natural Language Expense Parsing

Example:

```text
I paid 2400 for dinner split equally between me Aman and Priya

Tech Stack
Layer	Technology
Backend	FastAPI
Frontend	Streamlit
Database	SQLite
ORM	SQLAlchemy
AI	Ollama + TinyLlama
Validation	Pydantic
Project Structure
splitexpense/
│
├── server/
│   ├── app/
│   │   ├── ai/
│   │   ├── algorithms/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── database.py
│   │   └── main.py
│   │
│   ├── frontend.py
│   └── requirements.txt
Installation
1. Clone Repository
git clone <your-repo-url>
cd splitexpense/server
2. Install Dependencies
pip install -r requirements.txt {includes liabraries like pydantics}
3. Install Ollama

Download:

https://ollama.com/download

4. Pull TinyLlama Model
ollama pull tinyllama{can also pull larger models}
Running the Project
Start Backend
uvicorn app.main:app --reload

Backend runs on:

http://127.0.0.1:8000

Swagger Docs:

http://127.0.0.1:8000/docs
Start Frontend

Open another terminal:

streamlit run frontend.py

Frontend runs on:

http://localhost:8501

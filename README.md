# Smart Expense Tracker API

A production-quality REST API built with **Python 3.12** and **FastAPI** for managing personal expenses. Data is persisted locally using a thread-safe JSON storage layer without requiring external database dependencies.

> 📖 **Non-Technical Reader?** Check out our plain-English guide: [NON_TECHNICAL_GUIDE.md](file:///Users/apple/My%20Projects/expense-tracker-api/NON_TECHNICAL_GUIDE.md) explaining how everything works using simple analogies!

---

Designed with clean modular architecture, separation of concerns (SOLID principles), Pydantic v2 data validation, and comprehensive automated test coverage.

---

## Features

- **Expense Management**: Create, view, filter, and delete expense records.
- **Auto-generated IDs**: Unique integer IDs assigned automatically upon expense creation.
- **Category Filtering**: Case-insensitive filtering on expenses list and expenditure totals.
- **Totals Calculation**: Calculate overall expenditure sum or total spent per category.
- **Strict Data Validation**: Validates non-empty title/category, positive amount (`> 0`), and ISO format date (`YYYY-MM-DD`).
- **Thread-safe Persistence**: Reads and writes to `expenses.json` protected by re-entrant file locks.
- **Interactive Swagger Documentation**: Auto-generated interactive API docs powered by FastAPI / OpenAPI.
- **Automated Test Suite**: Full integration test suite using `pytest` and `httpx`.

---

## Folder Structure

```
smart-expense-tracker-api/
│
├── README.md              # Project documentation and API guide
├── AI_NOTES.md            # Notes on AI assistance, validation, and production readiness
├── requirements.txt       # Python project dependencies
├── expenses.json          # Persistent local JSON data store
│
├── src/
│   ├── __init__.py        # Package initialization
│   ├── main.py            # FastAPI app setup, exception handlers, middleware
│   ├── models.py          # Pydantic schemas and payload validation rules
│   ├── routes.py          # REST API endpoints & route handlers
│   ├── storage.py         # Thread-safe JSON file storage interface
│   ├── services.py        # Business logic layer
│   └── utils.py          # Formatting & parsing utilities
│
└── tests/
    ├── __init__.py        # Test package initialization
    ├── test_create.py     # Expense creation & validation tests
    ├── test_get.py        # Expense listing tests
    ├── test_filter.py     # Category filtering tests
    ├── test_total.py      # Total calculations & category summary tests
    └── test_delete.py     # Expense deletion tests
```

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- `pip`

### Step 1: Clone or setup repository

```bash
cd smart-expense-tracker-api
```

### Step 2: Create & activate virtual environment

On **macOS / Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

On **Windows (PowerShell)**:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On **Windows (Command Prompt)**:
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the development server with live reload:

```bash
uvicorn src.main:app --reload
```

The application will be accessible at:
- **Base URL**: `http://localhost:8000`
- **Swagger UI Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Running Tests

Execute the automated test suite with `pytest`:

```bash
pytest
```

To run with verbose output:

```bash
pytest -v
```

---

## Example API Requests

### 1. Create an Expense (`POST /expenses`)

**Request**:
```bash
curl -X POST "http://localhost:8000/expenses" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lunch",
    "amount": 250.0,
    "category": "Food",
    "date": "2026-08-01"
  }'
```

**Response** (`201 Created`):
```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 250.0,
  "category": "Food",
  "date": "2026-08-01"
}
```

---

### 2. List All Expenses (`GET /expenses`)

**Request**:
```bash
curl -X GET "http://localhost:8000/expenses"
```

**Response** (`200 OK`):
```json
[
  {
    "id": 1,
    "title": "Lunch",
    "amount": 250.0,
    "category": "Food",
    "date": "2026-08-01"
  }
]
```

---

### 3. Filter Expenses by Category (`GET /expenses?category=Food`)

*Note: Filtering is case-insensitive.*

**Request**:
```bash
curl -X GET "http://localhost:8000/expenses?category=food"
```

**Response** (`200 OK`):
```json
[
  {
    "id": 1,
    "title": "Lunch",
    "amount": 250.0,
    "category": "Food",
    "date": "2026-08-01"
  }
]
```

---

### 4. Get Overall Total Expenses (`GET /expenses/total`)

**Request**:
```bash
curl -X GET "http://localhost:8000/expenses/total"
```

**Response** (`200 OK`):
```json
{
  "total": 1234.5
}
```

---

### 5. Get Total Expenses for a Category (`GET /expenses/total?category=Food`)

**Request**:
```bash
curl -X GET "http://localhost:8000/expenses/total?category=Food"
```

**Response** (`200 OK`):
```json
{
  "category": "Food",
  "total": 800.0
}
```

---

### 6. Delete an Expense (`DELETE /expenses/{id}`)

**Request**:
```bash
curl -X DELETE "http://localhost:8000/expenses/1"
```

**Response** (`200 OK`):
```json
{
  "message": "Expense deleted successfully"
}
```

If the ID does not exist (`404 Not Found`):
```json
{
  "detail": "Expense with ID 1 not found"
}
```

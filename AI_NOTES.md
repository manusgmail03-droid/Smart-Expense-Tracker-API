# AI Assistance Notes & Code Review Checklist

This document details how AI assistance was utilized during the development of the **Smart Expense Tracker API**, key areas recommended for manual review, and architectural trade-offs evaluated during development.

---

## 1. AI-Assisted Components

AI was utilized as a collaborative pair programming partner for the following tasks:

- **Boilerplate & Architecture Generation**: Structuring the modular codebase across `models`, `storage`, `services`, `routes`, and `utils`.
- **Pydantic Validation**: Writing standard validators for string trimming, positive float enforcement (`gt=0`), and ISO date handling.
- **FastAPI Exception Handling**: Mapping FastAPI default 422 `RequestValidationError` responses to HTTP 400 Bad Request to meet exact assignment specifications.
- **Test Suite Scaffolding**: Generating unit and integration test fixtures using `pytest` and FastAPI `TestClient` with temporary file isolation.
- **Documentation**: Drafting OpenAPI/Swagger metadata, endpoint descriptions, and markdown documentation (`README.md`).

---

## 2. Recommended Manual Review Points

Before deploying or submitting, a developer should manually review:

1. **File I/O Concurrency**: The current `storage.py` implementation uses Python's `threading.Lock()` for thread safety within a single process. If deploying with multi-worker Uvicorn processes (`uvicorn --workers 4`), file locking should be upgraded to inter-process file locks (`fcntl.flock` on Unix or `portalocker`).
2. **Precision of Floating-Point Calculations**: Expenses are represented as `float`. In high-precision financial systems, using Python's `decimal.Decimal` is preferred to prevent IEEE 754 floating-point rounding inaccuracies.
3. **Data Volume Limits**: The `expenses.json` store loads the entire file into memory for read/write operations. For large datasets (> 50,000 records), pagination and streaming/indexing become necessary.

---

## 3. Production Readiness Improvements

To transition this assignment submission into a production-grade enterprise microservice, consider the following enhancements:

- **Authentication & Authorization**: Integrate OAuth2 / JWT bearer tokens to isolate expenses per authenticated user (`user_id`).
- **Structured Logging & Tracing**: Replace basic `logging` with structured JSON logging (`structlog`) and OpenTelemetry instrumentation.
- **Pagination & Sorting**: Add `limit`, `offset`, and `sort_by` query parameters to `GET /expenses`.
- **CI/CD Pipeline**: Add GitHub Actions workflow for linting (`ruff`, `mypy`) and running `pytest`.
- **Dockerization**: Provide a `Dockerfile` and `docker-compose.yml` for multi-stage container builds.

---

## 4. AI Suggestion Intentionally Not Used: SQLite Database Integration

During the initial design phase, AI suggested using an **SQLite** database with SQLAlchemy / SQLModel ORM to handle concurrency, indexing, relational queries, and ACID transactions natively.

**Reason for Rejection**:
The assignment prompt explicitly required local **JSON file storage** (`expenses.json`) without external database engines (`NO database`). Therefore, SQLite was deliberately omitted, and a custom thread-safe `JSONStorage` manager was implemented instead to adhere strictly to the project constraints while maintaining code cleanliness and testability.

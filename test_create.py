"""Tests for creating expenses and payload validation."""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from src.main import app
from src.routes import get_expense_service
from src.services import ExpenseService
from src.storage import JSONStorage


@pytest.fixture
def client(tmp_path: Path):
    """Fixture to provide TestClient with isolated temporary JSON storage."""
    test_file = tmp_path / "test_expenses.json"
    storage = JSONStorage(file_path=test_file)
    service = ExpenseService(storage=storage)

    app.dependency_overrides[get_expense_service] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_expense_success(client: TestClient):
    """Test successful creation of a valid expense record."""
    payload = {
        "title": "Lunch",
        "amount": 250.0,
        "category": "Food",
        "date": "2026-08-01",
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 250.0
    assert data["category"] == "Food"
    assert data["date"] == "2026-08-01"


def test_create_expense_invalid_amount(client: TestClient):
    """Test creation with invalid zero or negative amount returns HTTP 400."""
    payload_zero = {
        "title": "Coffee",
        "amount": 0,
        "category": "Food",
        "date": "2026-08-01",
    }
    response_zero = client.post("/expenses", json=payload_zero)
    assert response_zero.status_code == 400

    payload_negative = {
        "title": "Coffee",
        "amount": -50.0,
        "category": "Food",
        "date": "2026-08-01",
    }
    response_neg = client.post("/expenses", json=payload_negative)
    assert response_neg.status_code == 400


def test_create_expense_missing_title(client: TestClient):
    """Test creation with missing or whitespace title returns HTTP 400."""
    payload_missing = {
        "amount": 100.0,
        "category": "Utilities",
        "date": "2026-08-01",
    }
    response_missing = client.post("/expenses", json=payload_missing)
    assert response_missing.status_code == 400

    payload_empty = {
        "title": "   ",
        "amount": 100.0,
        "category": "Utilities",
        "date": "2026-08-01",
    }
    response_empty = client.post("/expenses", json=payload_empty)
    assert response_empty.status_code == 400


def test_create_expense_invalid_date(client: TestClient):
    """Test creation with malformed date format returns HTTP 400."""
    payload = {
        "title": "Taxi",
        "amount": 45.0,
        "category": "Transport",
        "date": "01-08-2026",  # Not YYYY-MM-DD
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 400

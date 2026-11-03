"""Tests for total expense calculations."""

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


def test_total_calculation_empty(client: TestClient):
    """Test total calculation when no expenses exist."""
    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json() == {"total": 0.0}


def test_total_calculation_all(client: TestClient):
    """Test total calculation across all categories."""
    client.post("/expenses", json={"title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Dinner", "amount": 550.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Flight", "amount": 434.50, "category": "Travel", "date": "2026-08-01"})

    response = client.get("/expenses/total")
    assert response.status_code == 200
    assert response.json() == {"total": 1234.50}


def test_total_calculation_by_category(client: TestClient):
    """Test total calculation filtered by category."""
    client.post("/expenses", json={"title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Dinner", "amount": 550.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Flight", "amount": 434.50, "category": "Travel", "date": "2026-08-01"})

    response = client.get("/expenses/total?category=Food")
    assert response.status_code == 200
    assert response.json() == {"category": "Food", "total": 800.0}

    # Case-insensitive category query "food"
    response_lower = client.get("/expenses/total?category=food")
    assert response_lower.status_code == 200
    assert response_lower.json() == {"category": "food", "total": 800.0}

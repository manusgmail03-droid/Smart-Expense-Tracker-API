"""Tests for listing expenses."""

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


def test_get_expenses_empty(client: TestClient):
    """Test retrieving expenses list when storage is empty."""
    response = client.get("/expenses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_expenses(client: TestClient):
    """Test retrieving all expenses from storage."""
    exp1 = {"title": "Coffee", "amount": 15.0, "category": "Food", "date": "2026-08-01"}
    exp2 = {"title": "Subway", "amount": 30.0, "category": "Transport", "date": "2026-08-01"}

    client.post("/expenses", json=exp1)
    client.post("/expenses", json=exp2)

    response = client.get("/expenses")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert items[0]["title"] == "Coffee"
    assert items[1]["title"] == "Subway"

"""Tests for deleting expenses."""

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


def test_delete_expense_success(client: TestClient):
    """Test successful deletion of an existing expense."""
    create_res = client.post(
        "/expenses",
        json={"title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-08-01"},
    )
    expense_id = create_res.json()["id"]

    delete_res = client.delete(f"/expenses/{expense_id}")
    assert delete_res.status_code == 200
    assert delete_res.json() == {"message": "Expense deleted successfully"}

    # Verify expense is no longer returned in GET /expenses
    list_res = client.get("/expenses")
    assert list_res.status_code == 200
    assert list_res.json() == []


def test_delete_non_existent_expense(client: TestClient):
    """Test deleting a non-existent expense ID returns HTTP 404."""
    response = client.delete("/expenses/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Expense with ID 99999 not found"

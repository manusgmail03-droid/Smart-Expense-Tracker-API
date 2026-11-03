"""Tests for category filtering."""

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


def test_category_filter_case_insensitive(client: TestClient):
    """Test filtering expenses by category with case-insensitive query parameter."""
    client.post("/expenses", json={"title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Dinner", "amount": 550.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus", "amount": 20.0, "category": "Transport", "date": "2026-08-01"})

    # Case 1: Exact case query "Food"
    res1 = client.get("/expenses?category=Food")
    assert res1.status_code == 200
    items1 = res1.json()
    assert len(items1) == 2

    # Case 2: Lowercase query "food"
    res2 = client.get("/expenses?category=food")
    assert res2.status_code == 200
    items2 = res2.json()
    assert len(items2) == 2

    # Case 3: Uppercase query "FOOD"
    res3 = client.get("/expenses?category=FOOD")
    assert res3.status_code == 200
    items3 = res3.json()
    assert len(items3) == 2


def test_category_filter_no_match(client: TestClient):
    """Test filtering by category with no matching records returns empty list."""
    client.post("/expenses", json={"title": "Lunch", "amount": 250.0, "category": "Food", "date": "2026-08-01"})
    
    res = client.get("/expenses?category=Entertainment")
    assert res.status_code == 200
    assert res.json() == []

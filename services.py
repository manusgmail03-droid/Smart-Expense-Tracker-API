"""Business logic service for managing expenses."""

from typing import List, Optional, Tuple, Dict, Any
from src.models import (
    ExpenseCreate,
    ExpenseResponse,
    TotalResponse,
    CategoryTotalResponse,
)
from src.storage import JSONStorage
from src.utils import format_amount, parse_date


class ExpenseService:
    """Service layer executing business operations on expenses."""

    def __init__(self, storage: Optional[JSONStorage] = None) -> None:
        """Initialize service with storage provider.

        Args:
            storage: Optional custom JSONStorage instance. Defaults to standard storage.
        """
        self.storage = storage or JSONStorage()

    def create_expense(self, expense_in: ExpenseCreate) -> ExpenseResponse:
        """Create and persist a new expense.

        Args:
            expense_in: Expense creation schema data.

        Returns:
            Created ExpenseResponse model with auto-generated ID.
        """
        data = {
            "title": expense_in.title,
            "amount": format_amount(expense_in.amount),
            "category": expense_in.category,
            "date": parse_date(expense_in.date),
        }
        created_dict = self.storage.add(data)
        return ExpenseResponse(**created_dict)

    def get_expenses(self, category: Optional[str] = None) -> List[ExpenseResponse]:
        """Retrieve list of expenses, optionally filtered by category (case-insensitive).

        Args:
            category: Optional category filter string.

        Returns:
            List of matching ExpenseResponse models.
        """
        all_raw = self.storage.read_all()
        
        if category and category.strip():
            target_category = category.strip().lower()
            filtered_raw = [
                item for item in all_raw
                if item.get("category", "").strip().lower() == target_category
            ]
        else:
            filtered_raw = all_raw

        return [ExpenseResponse(**item) for item in filtered_raw]

    def get_total(
        self, category: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Calculate total expenditure, globally or for a specific category.

        Args:
            category: Optional category filter string.

        Returns:
            Tuple of (is_category_filtered: bool, result_dict: dict).
        """
        all_raw = self.storage.read_all()

        if category and category.strip():
            clean_category = category.strip()
            target = clean_category.lower()
            filtered = [
                item for item in all_raw
                if item.get("category", "").strip().lower() == target
            ]
            total_sum = sum(item.get("amount", 0.0) for item in filtered)
            return True, {
                "category": clean_category,
                "total": format_amount(total_sum),
            }

        total_sum = sum(item.get("amount", 0.0) for item in all_raw)
        return False, {"total": format_amount(total_sum)}

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense record by ID.

        Args:
            expense_id: Unique integer identifier.

        Returns:
            True if expense was found and deleted, False otherwise.
        """
        return self.storage.delete(expense_id)

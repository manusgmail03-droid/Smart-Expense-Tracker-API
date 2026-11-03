"""Thread-safe JSON file storage layer for expense persistence."""

import json
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any, Optional


class JSONStorage:
    """Handles read and write operations to a local JSON file store with thread safety."""

    def __init__(self, file_path: Optional[Path] = None) -> None:
        """Initialize storage manager.

        Args:
            file_path: Optional custom path to JSON file. Defaults to 'expenses.json' in project root.
        """
        if file_path is None:
            # Default to expenses.json in root directory
            self.file_path = Path(__file__).resolve().parent.parent / "expenses.json"
        else:
            self.file_path = Path(file_path)

        self._lock = Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure destination JSON file exists and contains valid JSON array."""
        with self._lock:
            if not self.file_path.exists():
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=2)
            else:
                try:
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                except (json.JSONDecodeError, OSError):
                    data = []
                
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

    def read_all(self) -> List[Dict[str, Any]]:
        """Read and return all expenses from the JSON file.

        Returns:
            List of expense dictionaries.
        """
        with self._lock:
            if not self.file_path.exists():
                return []
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []

    def write_all(self, expenses: List[Dict[str, Any]]) -> None:
        """Overwrite the JSON file with the updated list of expenses.

        Args:
            expenses: Complete list of expense dictionaries to persist.
        """
        with self._lock:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(expenses, f, indent=2, ensure_ascii=False)

    def add(self, expense_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new expense record with an auto-generated integer ID.

        Args:
            expense_data: Dictionary containing expense attributes without ID.

        Returns:
            The created expense dictionary containing the new ID.
        """
        expenses = self.read_all()
        next_id = max([e.get("id", 0) for e in expenses], default=0) + 1
        new_expense = {"id": next_id, **expense_data}
        expenses.append(new_expense)
        self.write_all(expenses)
        return new_expense

    def delete(self, expense_id: int) -> bool:
        """Delete an expense record by its ID.

        Args:
            expense_id: Unique integer ID of the expense to delete.

        Returns:
            True if deleted, False if ID was not found.
        """
        expenses = self.read_all()
        initial_count = len(expenses)
        filtered_expenses = [e for e in expenses if e.get("id") != expense_id]
        
        if len(filtered_expenses) == initial_count:
            return False

        self.write_all(filtered_expenses)
        return True

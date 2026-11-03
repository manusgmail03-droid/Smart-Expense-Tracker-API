"""Utility functions for data formatting, date validation, and rounding."""

from datetime import datetime, date
from typing import Union


def format_amount(amount: float) -> float:
    """Format and round currency amounts to 2 decimal places.

    Args:
        amount: The float amount to round.

    Returns:
        Rounded float value up to 2 decimal places.
    """
    return round(float(amount), 2)


def parse_date(date_input: Union[str, date]) -> str:
    """Parse date input into ISO YYYY-MM-DD string format.

    Args:
        date_input: String or date object representing the expense date.

    Returns:
        Formatted string YYYY-MM-DD.

    Raises:
        ValueError: If string format is invalid.
    """
    if isinstance(date_input, date):
        return date_input.isoformat()
    
    # Try parsing string to ensure YYYY-MM-DD
    parsed = datetime.strptime(date_input, "%Y-%m-%d").date()
    return parsed.isoformat()

"""Data models and schemas for Smart Expense Tracker API."""

from datetime import date as DateType
from pydantic import BaseModel, Field, field_validator


class ExpenseBase(BaseModel):
    """Base schema for expense data."""

    title: str = Field(..., description="Title or description of the expense", json_schema_extra={"example": "Lunch"})
    amount: float = Field(..., gt=0, description="Amount spent, must be greater than 0", json_schema_extra={"example": 250.0})
    category: str = Field(..., description="Category of the expense", json_schema_extra={"example": "Food"})
    date: DateType = Field(..., description="Date of the expense in YYYY-MM-DD format", json_schema_extra={"example": "2026-08-01"})

    @field_validator("title", "category")
    @classmethod
    def validate_non_empty_str(cls, value: str) -> str:
        """Ensure title and category are not empty strings or whitespace only."""
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty or whitespace only")
        return cleaned


class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense."""

    pass


class ExpenseResponse(ExpenseBase):
    """Schema for returning expense details including auto-generated ID."""

    id: int = Field(..., description="Unique auto-generated ID of the expense", json_schema_extra={"example": 1})

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Lunch",
                "amount": 250.0,
                "category": "Food",
                "date": "2026-08-01"
            }
        }
    }


class TotalResponse(BaseModel):
    """Schema for returning total calculation across all expenses."""

    total: float = Field(..., description="Total sum of expenses", json_schema_extra={"example": 1234.50})


class CategoryTotalResponse(BaseModel):
    """Schema for returning total calculation filtered by a category."""

    category: str = Field(..., description="Target category", json_schema_extra={"example": "Food"})
    total: float = Field(..., description="Total sum of expenses for category", json_schema_extra={"example": 800.0})


class MessageResponse(BaseModel):
    """Generic message response schema."""

    message: str = Field(..., description="Status message", json_schema_extra={"example": "Expense deleted successfully"})

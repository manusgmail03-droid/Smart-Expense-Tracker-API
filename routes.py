"""API route definitions for Smart Expense Tracker API."""

from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.models import (
    ExpenseCreate,
    ExpenseResponse,
    TotalResponse,
    CategoryTotalResponse,
    MessageResponse,
)
from src.services import ExpenseService


router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_expense_service() -> ExpenseService:
    """Dependency provider for ExpenseService."""
    return ExpenseService()


@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense",
    description="Create a new expense item with title, amount (>0), category, and valid date (YYYY-MM-DD).",
)
def create_expense(
    expense: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
) -> ExpenseResponse:
    """Create a new expense record."""
    try:
        return service.create_expense(expense)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.get(
    "",
    response_model=List[ExpenseResponse],
    status_code=status.HTTP_200_OK,
    summary="List all expenses",
    description="Retrieve all expense records, optionally filtered by category (case-insensitive).",
)
def get_expenses(
    category: Optional[str] = Query(
        None,
        description="Filter expenses by category (case-insensitive)",
        examples=["Food"],
    ),
    service: ExpenseService = Depends(get_expense_service),
) -> List[ExpenseResponse]:
    """Retrieve expenses list."""
    return service.get_expenses(category=category)


@router.get(
    "/total",
    response_model=Union[CategoryTotalResponse, TotalResponse],
    status_code=status.HTTP_200_OK,
    summary="Calculate total expenses",
    description="Calculate the total sum of all expenses or expenses filtered by category.",
)
def get_total_expenses(
    category: Optional[str] = Query(
        None,
        description="Category filter for total calculation (case-insensitive)",
        examples=["Food"],
    ),
    service: ExpenseService = Depends(get_expense_service),
) -> Union[CategoryTotalResponse, TotalResponse]:
    """Calculate total sum of expenses."""
    is_category_filtered, result_data = service.get_total(category=category)
    if is_category_filtered:
        return CategoryTotalResponse(**result_data)
    return TotalResponse(**result_data)


@router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete an expense",
    description="Delete an existing expense by its unique ID.",
)
def delete_expense(
    id: int,
    service: ExpenseService = Depends(get_expense_service),
) -> MessageResponse:
    """Delete expense by ID."""
    deleted = service.delete_expense(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {id} not found",
        )
    return MessageResponse(message="Expense deleted successfully")

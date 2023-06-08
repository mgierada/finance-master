from datetime import datetime
import json
from database import get_db
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from middleware.validate_token import validate_token
from services.convert_to_dataframe import get_all_transactions_dataframe
from services.finance_analyzer.categories import (
    get_data_by_category,
)
from services.finance_analyzer.process_data import (
    get_expense_data_per_month,
    get_expense_data_per_year,
    get_income_data_per_month,
    get_income_data_per_year,
)
from sqlalchemy.orm import Session

router = APIRouter()


def _get_current_month_number():
    """
    Returns the current month as an integer.
    """
    return datetime.now().month


def _get_current_year_number():
    """
    Returns the current year as an integer.
    """
    return datetime.now().year


@router.get("/monthly/expenses")
async def monthly_expenses_by_categories(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    month: int = _get_current_month_number(),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    monthly_expense_data = get_expense_data_per_month(all_transactions_df, month, year)
    monthly_expenses_by_categories = get_data_by_category(monthly_expense_data)
    json_data = monthly_expenses_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    month_name = datetime.strptime(f"{month}", "%m").strftime("%B")
    content = {
        "message": f"Expenses by categories for month {month_name} of a year {year}",
        "data": data,
    }
    return JSONResponse(content=content)


@router.get("/yearly/expenses")
async def yearly_expenses_by_categories(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    yearly_expense_data = get_expense_data_per_year(all_transactions_df, year)
    yearly_expenses_by_categories = get_data_by_category(yearly_expense_data)
    json_data = yearly_expenses_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    content = {
        "message": f"Expenses by categories for the year {year}",
        "data": data,
    }
    return JSONResponse(content=content)


@router.get("/monthly/income")
async def monthly_income_by_categories(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    month: int = _get_current_month_number(),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    monthly_income_data = get_income_data_per_month(all_transactions_df, month, year)
    monthly_income_by_categories = get_data_by_category(monthly_income_data)
    json_data = monthly_income_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    month_name = datetime.strptime(f"{month}", "%m").strftime("%B")
    content = {
        "message": f"Income by categories for month {month_name} of a year {year}",
        "data": data,
    }
    return JSONResponse(content=content)


@router.get("/yearly/income")
async def yearly_income_by_categories(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    yearly_income_data = get_income_data_per_year(all_transactions_df, year)
    yearly_income_by_categories = get_data_by_category(yearly_income_data)
    json_data = yearly_income_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    content = {
        "message": f"Expenses by categories for the year {year}",
        "data": data,
    }
    return JSONResponse(content=content)

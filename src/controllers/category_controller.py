from datetime import datetime
import json
from database import get_db
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from services.convert_to_dataframe import get_all_transactions_dataframe
from services.finance_analyzer.categories import (
    get_monthly_data_by_categories_per_month,
)
from services.finance_analyzer.process_data import (
    get_expense_data_per_month,
    get_income_data_per_month,
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


@router.get("/expenses")
async def monthly_expenses_by_categories(
    db: Session = Depends(get_db),
    month: int = _get_current_month_number(),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    monthly_expense_data = get_expense_data_per_month(all_transactions_df, month, year)
    monthly_expenses_by_categories = get_monthly_data_by_categories_per_month(
        monthly_expense_data
    )
    json_data = monthly_expenses_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    month_name = datetime.strptime(f"{month}", "%m").strftime("%B")
    content = {
        "message": f"Expenses by categories for month {month_name} of year {year}",
        "data": data,
    }
    return JSONResponse(content=content)


@router.get("/income")
async def monthly_income_by_categories(
    db: Session = Depends(get_db),
    month: int = _get_current_month_number(),
    year: int = _get_current_year_number(),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    monthly_income_data = get_income_data_per_month(all_transactions_df, month, year)
    monthly_income_by_categories = get_monthly_data_by_categories_per_month(
        monthly_income_data
    )
    json_data = monthly_income_by_categories.to_json(orient="table")
    data = json.loads(json_data)["data"]
    month_name = datetime.strptime(f"{month}", "%m").strftime("%B")
    content = {
        "message": f"Income by categories for month {month_name} of year {year}",
        "data": data,
    }
    return JSONResponse(content=content)

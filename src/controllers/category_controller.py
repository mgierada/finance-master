import json
from database import get_db
from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from services.convert_to_dataframe import get_all_transactions_dataframe
from services.finance_analyzer.categories import get_monthly_expenses_by_categories
from services.finance_analyzer.process_data import get_expense_data
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/")
async def monthly_expenses_by_categories(
    db: Session = Depends(get_db),
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    expense_data = get_expense_data(all_transactions_df)
    monthly_expenses_by_categories = get_monthly_expenses_by_categories(expense_data)
    json_data = monthly_expenses_by_categories.to_json(orient="table")
    return JSONResponse(content=json.loads(json_data)["data"])

import json
import crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from services.convert_to_dataframe import convert_db_query_to_dataframe
from services.finance_analyzer.tax import get_expense_zus
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/zus")
async def get_zus_expenses_controller(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    all_transactions_df = convert_db_query_to_dataframe(all_transactions)
    zus_expenses = get_expense_zus(all_transactions_df)
    json_data = zus_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

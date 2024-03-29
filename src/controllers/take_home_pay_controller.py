import json
import crud
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from middleware.validate_token import validate_token
from services.convert_to_dataframe import convert_db_query_to_dataframe
from services.finance_analyzer.constants import CONST_EXPENSES
from services.finance_analyzer.take_home_pay import get_take_home_pay_monthly
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/")
async def take_home_pay_monthly(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    all_transactions_df = convert_db_query_to_dataframe(all_transactions)
    take_home_pay_monthly = get_take_home_pay_monthly(all_transactions_df)
    json_data = take_home_pay_monthly.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": f"Take home pay monthly as a difference between income and constant expenses {CONST_EXPENSES}",
            "data": json.loads(json_data)["data"],
        }
    )

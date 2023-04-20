import json
import crud
from database import get_db
import pandas as pd

from fastapi.responses import JSONResponse
from finance_analyzer.read_data import (
    get_summary_by_month,
    get_summary_by_year,
    read_and_clean_data,
)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/monthly")
async def summary_monthly(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    print(all_transactions)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    # convert all_transactions to list of dicts
    all_transactions = [transaction.__dict__ for transaction in all_transactions]
    # drop _sa_instance_state and id keys
    all_transactions = [
        {
            key: value
            for key, value in transaction.items()
            if key != "_sa_instance_state" and key != "id"
        }
        for transaction in all_transactions
    ]

    all_transactions_df = pd.DataFrame(all_transactions)
    all_transactions_df["date"] = pd.to_datetime(all_transactions_df["date"])
    summary_by_month = get_summary_by_month(all_transactions_df)
    json_data = summary_by_month.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])


@router.get("/yearly")
async def summary_yearly(with_schema: bool = False) -> JSONResponse:
    df = read_and_clean_data()
    summary_by_year = get_summary_by_year(df)
    json_data = summary_by_year.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

import json
import crud
from database import get_db

from fastapi.responses import JSONResponse
from finance_analyzer.read_data import (
    get_summary_by_month,
    get_summary_by_year,
    read_and_clean_data,
)

from fastapi import APIRouter, Depends, HTTPException
from services.convert_to_dataframe import convert_db_query_to_dataframe
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/monthly")
async def summary_monthly(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    all_transactions_df = convert_db_query_to_dataframe(all_transactions)
    summary_by_month = get_summary_by_month(all_transactions_df)
    json_data = summary_by_month.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])


@router.get("/yearly")
async def summary_yearly(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    all_transactions_df = convert_db_query_to_dataframe(all_transactions)
    summary_by_year = get_summary_by_year(all_transactions_df)
    json_data = summary_by_year.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

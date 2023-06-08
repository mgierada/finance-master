import json
from database import get_db

from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from middleware.validate_token import validate_token
from services.convert_to_dataframe import (
    get_all_transactions_dataframe,
)
from services.finance_analyzer.process_data import (
    get_summary_by_month,
    get_summary_by_year,
)
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/monthly")
async def summary_monthly(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    summary_by_month = get_summary_by_month(all_transactions_df)
    json_data = summary_by_month.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])


@router.get("/yearly")
async def summary_yearly(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    summary_by_year = get_summary_by_year(all_transactions_df)
    json_data = summary_by_year.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

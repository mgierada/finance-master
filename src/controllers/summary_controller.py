import json

from fastapi.responses import JSONResponse
from finance_analyzer.read_data import (
    get_summary_by_month,
    get_summary_by_year,
    read_and_clean_data,
)

from fastapi import APIRouter

router = APIRouter()


@router.get("/monthly")
async def summary_monthly(with_schema: bool = False) -> JSONResponse:
    df = read_and_clean_data()
    summary_by_month = get_summary_by_month(df)
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

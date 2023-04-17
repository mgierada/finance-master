import json

from fastapi.responses import JSONResponse
from finance_analyzer.read_data import get_summary_by_month, read_and_clean_data

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    df = read_and_clean_data()
    summary_by_month = get_summary_by_month(df)
    json_data = summary_by_month.to_json(orient="table")
    return JSONResponse(content=json.loads(json_data))

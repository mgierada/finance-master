import json

from fastapi.responses import JSONResponse
from finance_analyzer.read_data import (
    read_and_clean_data,
)

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def tranactions(with_schema: bool = False) -> JSONResponse:
    df = read_and_clean_data()
    json_data = df.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

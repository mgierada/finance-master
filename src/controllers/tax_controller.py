import json
from database import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services.convert_to_dataframe import (
    get_all_transactions_dataframe,
)
from services.finance_analyzer.tax import (
    get_expenses_zus,
    get_expenses_vat7,
    get_expenses_vat_ppe,
)
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/zus")
async def get_expenses_zus_controller(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    zus_expenses = get_expenses_zus(all_transactions_df)
    json_data = zus_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])


@router.get("/vat-7")
async def get_expenses_vat7_controller(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat7expenses = get_expenses_vat7(all_transactions_df)
    json_data = vat7expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])


@router.get("/vat-ppe")
async def get_expenses_vat_ppe_controller(
    db: Session = Depends(get_db), with_schema: bool = False
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat_ppe_expenses = get_expenses_vat_ppe(all_transactions_df)
    json_data = vat_ppe_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(content=json.loads(json_data)["data"])

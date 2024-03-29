import json
from database import get_db
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from middleware.validate_token import validate_token
from services.convert_to_dataframe import (
    get_all_transactions_dataframe,
)
from services.finance_analyzer.constants import UNWANTED_FIELDS_TAX_RESPONSE
from services.finance_analyzer.tax import (
    get_expenses_zus,
    get_expenses_vat7,
    get_expenses_vat_ppe,
    get_expenses_zus_total_per_year,
    get_expenses_vat7_total_per_year,
    get_expenses_vat_ppe_total_per_year,
)
from sqlalchemy.orm import Session
from utils.utils import filter_unwanted_fields_from_dict


router = APIRouter()


@router.get("/zus")
async def get_expenses_zus_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    zus_expenses = get_expenses_zus(all_transactions_df)
    json_data = zus_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "ZUS expenses per month",
            "data": list(
                map(
                    lambda x: filter_unwanted_fields_from_dict(
                        x, UNWANTED_FIELDS_TAX_RESPONSE
                    ),
                    json.loads(json_data)["data"],
                )
            ),
        }
    )


@router.get("/zus/total")
async def get_expenses_zus_total_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    zus_expenses_total = get_expenses_zus_total_per_year(all_transactions_df)
    json_data = zus_expenses_total.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "ZUS expenses per year",
            "data": json.loads(json_data)["data"],
        }
    )


@router.get("/vat-7")
async def get_expenses_vat7_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat7_expenses = get_expenses_vat7(all_transactions_df)
    json_data = vat7_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "VAT-7 expenses per month",
            "data": list(
                map(
                    lambda x: filter_unwanted_fields_from_dict(
                        x, UNWANTED_FIELDS_TAX_RESPONSE
                    ),
                    json.loads(json_data)["data"],
                )
            ),
        }
    )


@router.get("/vat-7/total")
async def get_expenses_vat7_total_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat7_expenses_total = get_expenses_vat7_total_per_year(all_transactions_df)
    json_data = vat7_expenses_total.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "VAT-7 expenses per year",
            "data": json.loads(json_data)["data"],
        }
    )


@router.get("/vat-ppe")
async def get_expenses_vat_ppe_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat_ppe_expenses = get_expenses_vat_ppe(all_transactions_df)
    json_data = vat_ppe_expenses.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "VAT PPE expenses per month",
            "data": list(
                map(
                    lambda x: filter_unwanted_fields_from_dict(
                        x, UNWANTED_FIELDS_TAX_RESPONSE
                    ),
                    json.loads(json_data)["data"],
                )
            ),
        }
    )


@router.get("/vat-ppe/total")
async def get_expenses_vat_ppe_total_controller(
    _: str = Depends(validate_token),
    db: Session = Depends(get_db),
    with_schema: bool = False,
) -> JSONResponse:
    all_transactions_df = get_all_transactions_dataframe(db)
    vat_ppe_expenses_total = get_expenses_vat_ppe_total_per_year(all_transactions_df)
    json_data = vat_ppe_expenses_total.to_json(orient="table")
    if with_schema:
        return JSONResponse(content=json.loads(json_data))
    return JSONResponse(
        content={
            "message": "VAT PPE expenses per year",
            "data": json.loads(json_data)["data"],
        }
    )

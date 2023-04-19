import json
import crud
from database import get_db
from fastapi.responses import JSONResponse

from finance_analyzer.read_data import (
    read_and_clean_data,
)

from fastapi import APIRouter, Depends
import schemas
from sqlalchemy.orm import Session
from utils.check_cuplicates import is_entry_already_in_db

from utils.convert_data import convert_date

router = APIRouter()


@router.post("/populate", response_model=schemas.Transactions)
async def populate_db(db: Session = Depends(get_db)) -> JSONResponse:
    df = read_and_clean_data()
    json_data = df.to_json(orient="table")

    raw_payloads = json.loads(json_data)["data"]
    for raw_payload in raw_payloads:
        # create a new TransactionCreate object
        transaction_create = schemas.TransactionCreate(
            date=convert_date(raw_payload["date"]),
            description=raw_payload["description"],
            account=raw_payload["account"],
            category=raw_payload["category"],
            amount=int(raw_payload["amount"]),  # convert to int
            currency=raw_payload["currency"],
        )
        # If date, category and amount and description already exists in db, skip that transaction
        if is_entry_already_in_db(db, transaction_create):
            # return JSONResponse(content={"message": "Entry already exists"})
            continue
        # return crud.create_transaction(db, transaction_create)
        crud.create_transaction(db, transaction_create)

    return JSONResponse(content={"message": "Entires added"})

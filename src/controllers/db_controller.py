import json
import uuid
import crud
from database import get_db
from fastapi.responses import JSONResponse

from finance_analyzer.read_data import (
    read_and_clean_data,
)

from fastapi import APIRouter, Depends
import schemas
from sqlalchemy.orm import Session

from utils.convert_data import convert_date

router = APIRouter()


@router.post("/populate", response_model=schemas.Transactions)
async def populate_db(db: Session = Depends(get_db)):
    df = read_and_clean_data()
    json_data = df.to_json(orient="table")

    raw_payload = json.loads(json_data)["data"][0]
    print("raw_payload")
    print(raw_payload)
    transaction = {"date": raw_payload["date"]}
    print("transaction")
    print(transaction)

    # create a new TransactionCreate object
    transaction_create = schemas.TransactionCreate(
        uuid=uuid.uuid4(),
        date=convert_date(raw_payload["date"]),
        description=raw_payload["description"],
        account=raw_payload["account"],
        category=raw_payload["category"],
        amount=int(raw_payload["amount"]),  # convert to int
        currency=raw_payload["currency"],
    )
    print("transaction_create")
    print(transaction_create.dict())

    # return crud.create_transaction(db, transaction)
    return crud.create_transaction(db, transaction_create)

    # return JSONResponse(content=json.loads(json_data)["data"])

import crud
from database import get_db
import typing as t

from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends
from middleware.validate_token import validate_token
import schemas
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=t.List[schemas.Transactions])
async def get_tranactions(
    token: str = Depends(validate_token),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
):
    return crud.get_transactions(db, skip, limit, retrieve_all_entries=False)


@router.delete("/")
async def remove_tranactions(db: Session = Depends(get_db)) -> JSONResponse:
    number_of_removed_transactions = crud.remove_transactions(db)
    return JSONResponse(
        content={"message": f"{number_of_removed_transactions} transactions removed"}
    )

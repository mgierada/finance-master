import crud
import schemas
from sqlalchemy.orm import Session


def is_entry_already_in_db(db: Session, transaction: schemas.TransactionCreate):
    dups = crud.filter_transactions(
        db,
        date=transaction.date,
        description=transaction.description,
        category=transaction.category,
        amount=transaction.amount,
    )
    return True if dups else False

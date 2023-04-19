from sqlalchemy.orm import Session
from models.transactions import Transaction

from schemas.transactions import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        date=transaction.date,
        description=transaction.description,
        account=transaction.account,
        category=transaction.category,
        amount=transaction.amount,
        currency=transaction.currency,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def filter_transactions(db: Session, **kwargs):
    return db.query(Transaction).filter_by(**kwargs).all()

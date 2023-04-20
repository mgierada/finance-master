from sqlalchemy.orm import Session
from models.transactions import Transaction
import typing as t
from schemas.transactions import TransactionCreate


def create_transaction(db: Session, transaction: TransactionCreate) -> Transaction:
    """Create a new transaction in the database

    Args:
        db (Session): The database session
        transaction (TransactionCreate): The transaction to be created
    Returns:
        Transaction: The created transaction
    """
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


def filter_transactions(db: Session, **kwargs) -> t.List[Transaction]:
    """Filter transactions by any of the following fields:
        - date
        - description
        - account
        - category
        - amount
        - currency

    Args:
        db (Session): The database session
        **kwargs: The fields to filter by
    Returns:
        t.List[Transaction]: The filtered transactions
    """
    return db.query(Transaction).filter_by(**kwargs).all()

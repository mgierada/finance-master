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


def get_transactions(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    retrieve_all_entries: bool = False,
) -> t.List[Transaction]:
    """Get all transactions from the database

    Args:
        db (Session): The database session
        retrieve_all_entries (bool, optional): Whether to retrieve all entries or not. Defaults to False.
        skip (int, optional): The number of entries to skip. Defaults to 0.
        limit (int, optional): The number of entries to retrieve. Defaults to 100.
    Returns:
        t.List[Transaction]: The transactions
    """
    return (
        db.query(Transaction).order_by(Transaction.date.desc()).all()
        if retrieve_all_entries
        else db.query(Transaction)
        .order_by(Transaction.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def remove_transactions(db: Session) -> int:
    """Remove all transactions from the database

    Args:
        db (Session): The database session
    Returns:
        int: The number of removed transactions
    """
    removed_transations = db.query(Transaction).delete()
    db.commit()
    return removed_transations

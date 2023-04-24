import crud
from fastapi import HTTPException
from models.transactions import Transaction
import pandas as pd
import typing as t

from sqlalchemy.orm import Session


def convert_db_query_to_dataframe(
    all_transactions: t.List[Transaction],
) -> pd.DataFrame:
    all_transactions_as_dict = [
        transaction.__dict__ for transaction in all_transactions
    ]
    # drop _sa_instance_state and id keys
    all_transactions_as_dict = [
        {
            key: value
            for key, value in transaction.items()
            if key != "_sa_instance_state" and key != "id"
        }
        for transaction in all_transactions_as_dict
    ]

    all_transactions_df = pd.DataFrame(all_transactions_as_dict)
    all_transactions_df["date"] = pd.to_datetime(all_transactions_df["date"])
    return all_transactions_df


def get_all_transactions_dataframe(db: Session) -> pd.DataFrame:
    all_transactions = crud.get_transactions(db, retrieve_all_entries=True)
    if not all_transactions:
        raise HTTPException(status_code=404, detail="No transactions found")
    return convert_db_query_to_dataframe(all_transactions)

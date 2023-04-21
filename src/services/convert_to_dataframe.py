from models.transactions import Transaction
import pandas as pd
import typing as t


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

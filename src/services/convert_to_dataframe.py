import pandas as pd


def convert_db_query_to_dataframe(all_transactions) -> pd.DataFrame:
    all_transactions = [transaction.__dict__ for transaction in all_transactions]
    # drop _sa_instance_state and id keys
    all_transactions = [
        {
            key: value
            for key, value in transaction.items()
            if key != "_sa_instance_state" and key != "id"
        }
        for transaction in all_transactions
    ]

    all_transactions_df = pd.DataFrame(all_transactions)
    all_transactions_df["date"] = pd.to_datetime(all_transactions_df["date"])
    return all_transactions_df

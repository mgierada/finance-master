import pandas as pd


def get_monthly_data_by_categories(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["category"])["amount"].sum().to_frame()

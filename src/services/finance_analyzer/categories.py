import pandas as pd


def get_monthly_data_by_categories_per_month(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(["category"])["amount"].sum().to_frame()

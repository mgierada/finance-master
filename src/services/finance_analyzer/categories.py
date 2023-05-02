import pandas as pd


def get_monthly_expenses_by_categories(df: pd.DataFrame) -> pd.DataFrame:
    df["month"] = df["date"].dt.strftime("%Y-%m")
    return df.groupby(["category", "month"])["amount"].sum().to_frame()

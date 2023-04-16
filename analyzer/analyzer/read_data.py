from analyzer.constants import COLUMNS
import pandas as pd


def read_and_clean_data() -> pd.DataFrame:
    raw_dataframe = pd.read_csv("data.csv", sep=";", index_col=False)
    raw_dataframe = raw_dataframe.rename(columns=COLUMNS)
    raw_dataframe["amount"] = raw_dataframe["raw_amount"].str.extract("([\d,-\. ]+)")
    raw_dataframe["amount"] = raw_dataframe["amount"].str.replace(" ", "")
    raw_dataframe["amount"] = (
        raw_dataframe["amount"].str.replace(",", ".").astype(float)
    )
    raw_dataframe["currency"] = raw_dataframe["raw_amount"].str.extract("([A-Z]{3})")
    clean_dataframe = raw_dataframe.drop(["raw_amount", "Unnamed: 5"], axis=1)
    return clean_dataframe


def get_income_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["amount"] > 0].set_index("date")


def get_spending_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["amount"] < 0].set_index("date")


def get_income_data_per_month(df: pd.DataFrame, month_number: int) -> pd.DataFrame:
    df = get_income_data(df)
    return get_data_per_month(df, month_number)


def get_spending_data_per_month(df: pd.DataFrame, month_number: int) -> pd.DataFrame:
    df = get_income_data(df)
    return get_data_per_month(df, month_number)


def get_data_per_month(df: pd.DataFrame, month_number: int) -> pd.DataFrame:
    # return df.groupby(pd.Grouper(freq="M")).sum()
    df.loc[:, "date"] = pd.to_datetime(df["date"])
    df[df["date"].dt.month == month_number]
    return df

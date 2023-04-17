from analyzer.constants import COLUMNS
import pandas as pd


def read_and_clean_data() -> pd.DataFrame:
    """
    Read the data from the csv file and clean it.
    """
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
    """
    For a given cleaned dataframe, return a dataframe with only the income data.
    """
    return df[df["amount"] > 0].set_index("date")


def get_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with only the expense data.
    """
    return df[df["amount"] < 0].set_index("date")


def get_income_data_per_month(
    df: pd.DataFrame, month_number: int, year: int
) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the income data for a given month and year.
    """
    income_date = get_income_data(df)
    return get_data_per_month(income_date, month_number, year)


def get_expense_data_per_month(
    df: pd.DataFrame, month_number: int, year: int
) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the expense data for a given month and year.
    """
    df = get_income_data(df)
    return get_data_per_month(df, month_number, year)


def get_data_per_month(df: pd.DataFrame, month_number: int, year: int) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the data for a given month and year.
    """
    df_copy = df.copy()
    df_copy.loc[:, "date"] = pd.to_datetime(df_copy["date"])
    df_copy["date"] = pd.to_datetime(df_copy["date"])
    return df_copy[
        (df_copy["date"].dt.month == month_number) & (df_copy["date"].dt.year == year)
    ]


def get_totals_all_months(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given income or expense dataframe, return a dataframe with the total amount of income or expense per month.
    """
    return df.groupby(df["date"].dt.strftime("%Y-%m"))["amount"].sum().to_frame()

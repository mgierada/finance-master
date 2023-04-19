import pandas as pd
import os
import typing as t

from finance_analyzer.constants import COLUMNS


def read_and_clean_data() -> pd.DataFrame:
    """
    Read the data from the csv file and clean it.
    """
    path_to_csv = os.path.join(os.path.dirname(__file__), "data.csv")
    raw_dataframe = pd.read_csv(path_to_csv, sep=";", index_col=False)
    raw_dataframe = raw_dataframe.rename(columns=COLUMNS)
    raw_dataframe["description"] = raw_dataframe["description"].apply(
        lambda x: " ".join(x.strip().split())
    )
    raw_dataframe["amount"] = raw_dataframe["raw_amount"].str.extract("([\d,-\. ]+)")
    raw_dataframe["amount"] = raw_dataframe["amount"].str.replace(" ", "")
    raw_dataframe["amount"] = (
        raw_dataframe["amount"].str.replace(",", ".").astype(float)
    )
    raw_dataframe["currency"] = raw_dataframe["raw_amount"].str.extract("([A-Z]{3})")
    clean_dataframe = raw_dataframe.drop(["raw_amount", "Unnamed: 5"], axis=1)
    df_copy = clean_dataframe.copy()
    df_copy["date"] = pd.to_datetime(df_copy["date"])
    return df_copy


def get_income_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with only the income data.
    """
    return df[df["amount"] > 0]


def get_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with only the expense data.
    """
    return df[df["amount"] < 0]


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
    df_copy["date"] = pd.to_datetime(df_copy["date"])
    return df_copy[
        (df_copy["date"].dt.month == month_number) & (df_copy["date"].dt.year == year)
    ]


def get_monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given income or expense dataframe, return a dataframe with the total amount of income or expense per month.
    """
    return df.groupby(df["date"].dt.strftime("%Y-%m"))["amount"].sum().to_frame()


def get_yearly_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given income or expense dataframe, return a dataframe with the total amount of income or
    expense per year.
    """
    return df.groupby(df["date"].dt.strftime("%Y"))["amount"].sum().to_frame()


def get_summary_by_month(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a summary dataframe with the total income and expense per
    month and other useful information.
    """
    income_data, expense_data = get_incomes_and_expenses(cleaned_df)
    income_totals = get_monthly_totals(income_data)
    expense_totals = get_monthly_totals(expense_data)
    return summary(income_totals, expense_totals)


def get_incomes_and_expenses(
    cleaned_df: pd.DataFrame,
) -> t.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    For a given cleaned dataframe, return a tuple with the income and expense dataframes.
    """
    return get_income_data(cleaned_df), get_expense_data(cleaned_df)


def get_summary_by_year(cleaned_df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a summary dataframe with the total income and expense per
    year and other useful information.
    """
    income_data, expense_data = get_incomes_and_expenses(cleaned_df)
    income_totals = get_yearly_totals(income_data)
    expense_totals = get_yearly_totals(expense_data)
    return summary(income_totals, expense_totals)


def summary(income_totals: pd.DataFrame, expense_totals: pd.DataFrame) -> pd.DataFrame:
    summary = pd.merge(expense_totals, income_totals, on="date")
    summary.rename(columns={"amount_x": "expense", "amount_y": "income"}, inplace=True)
    summary["expense_pct_change"] = summary["expense"].pct_change() * 100
    summary["income_pct_change"] = summary["income"].pct_change() * 100
    summary["profit"] = summary["income"] + summary["expense"]
    return summary.sort_values(by="date", ascending=False)


if __name__ == "__main__":
    df = read_and_clean_data()
    print(df)
    # summary_by_month = get_summary_by_month(df)
    # summary_by_year = get_summary_by_year(df)
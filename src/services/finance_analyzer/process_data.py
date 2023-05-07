import pandas as pd
import typing as t


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


def get_income_data_per_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the income data for a given year.
    """
    income_date = get_income_data(df)
    return get_data_per_year(income_date, year)


def get_expense_data_per_month(
    df: pd.DataFrame, month_number: int, year: int
) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the expense data for a given month and year.
    """
    expense_data = get_expense_data(df)
    return get_data_per_month(expense_data, month_number, year)


def get_expense_data_per_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the expense data for a given year.
    """
    expense_data = get_expense_data(df)
    return get_data_per_year(expense_data, year)


def get_data_per_month(df: pd.DataFrame, month_number: int, year: int) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the data for a given month and year.
    """
    return df[(df["date"].dt.month == month_number) & (df["date"].dt.year == year)]


def get_data_per_year(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the data for a given year.
    """
    return df[(df["date"].dt.year == year)]


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

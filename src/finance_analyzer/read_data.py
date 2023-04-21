from io import BytesIO
import pandas as pd
import typing as t

from finance_analyzer.constants import COLUMNS, COLUMNS_TO_BE_DROPPED, CSV_HEADER


def convert_bytes_to_dataframe(raw_csv_file: bytes) -> pd.DataFrame:
    """
    Read the data from the csv file, clean it and return as a dataframe.

    Args:
        csv_file: The csv file to be read as bytes.
    Returns:
        A pandas dataframe with the cleaned data from the csv file.
    """
    raw_dataframe = read_data(raw_csv_file)
    return clean_data(raw_dataframe)


def read_data(raw_csv_file: bytes) -> pd.DataFrame:
    """
    Read the data from the raw csv file and format it correctly.

    Args:
        csv_file: The csv file to be read as bytes.
    Returns:
        A pandas dataframe with the raw data from the csv file.
    """
    formatted_csv = format_data(raw_csv_file)
    return pd.read_csv(BytesIO(formatted_csv), sep=";", index_col=False)


def format_data(raw_csv_file: bytes) -> bytes:
    """
    Format the data from the csv file. The data is in bytes, and the first few lines are not part of
    the csv file.

    Args:
        csv_file: The csv file to be read as bytes.
    Returns:
        A bytes object with the formatted data from the csv file - removed some artifacts
    """
    # convert bytest to str
    raw_csv_file_as_str = raw_csv_file.decode("utf-8")
    # split by newline character
    lines = raw_csv_file_as_str.split("\n")
    # Find the index of the header row
    header_index = None
    for i, line in enumerate(lines):
        if line.startswith(CSV_HEADER):
            header_index = i
            break
    # join lines starting from the header index
    content = "\n".join(lines[header_index:])
    # convert to bytes
    return content.encode("utf-8")


def clean_data(raw_dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the data from the raw dataframe.

    Args:
        raw_dataframe: The raw dataframe with the data from the csv file.
    Returns:
        A pandas dataframe with the cleaned data from the csv file.
    """
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
    clean_dataframe = raw_dataframe.drop(COLUMNS_TO_BE_DROPPED, axis=1)
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

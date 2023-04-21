from io import BytesIO
import pandas as pd
import typing as t

from services.finance_analyzer.constants import (
    COLUMNS,
    COLUMNS_TO_BE_DROPPED,
    CSV_HEADER,
)


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

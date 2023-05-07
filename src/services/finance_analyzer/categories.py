import pandas as pd


def get_data_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe targeting selected data, return a dataframe with the data grouped
    by category.

    Args:
        df (pd.DataFrame): A dataframe with the data to be grouped by category.
    Returns:
        pd.DataFrame: A dataframe with the data grouped by category.
    """
    return df.groupby(["category"])["amount"].sum().to_frame()

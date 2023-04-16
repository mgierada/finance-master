from analyzer.constants import COLUMNS
import pandas as pd


def read_and_clean_data():
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


def get_income_data(df):
    return df[df["amount"] > 0]


def get_spending_data(df):
    return df[df["amount"] < 0]

from analyzer.constants import COLUMNS
import pandas as pd


def read_and_clean_data():
    df = pd.read_csv("data.csv", sep=";", index_col=False)
    df = df.rename(columns=COLUMNS)
    df["amount"] = df["raw_amount"].str.extract("([\d,-\. ]+)")
    df["amount"] = df["amount"].str.replace(" ", "")
    df["amount"] = df["amount"].str.replace(",", ".").astype(float)
    df["currency"] = df["raw_amount"].str.extract("([A-Z]{3})")
    df = df.drop(["raw_amount", "Unnamed: 5"], axis=1)
    return df

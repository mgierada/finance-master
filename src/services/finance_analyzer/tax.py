import pandas as pd
from services.finance_analyzer.constants import ZUS
from services.finance_analyzer.process_data import get_expense_data, get_income_data


def get_expense_zus(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of ZUS per month.
    """
    expense = get_expense_data(db)
    return expense[expense["description"].str.startswith(ZUS)]

import pandas as pd
from services.finance_analyzer.constants import ZUS, VAT7
from services.finance_analyzer.process_data import get_expense_data


def get_expenses_zus(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of ZUS.
    """
    expense = get_expense_data(db)
    return expense[expense["description"].str.startswith(ZUS)]


def get_expenses_vat7(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of VAT-7 payments.
    """
    expense = get_expense_data(db)
    return expense[expense["description"].str.contains(VAT7)]

import pandas as pd
from services.finance_analyzer.constants import ZUS, VAT_7, VAT_PPE
from services.finance_analyzer.process_data import get_expense_data, get_yearly_totals


def get_expenses_zus(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of ZUS.
    """
    expenses = get_expense_data(db)
    return expenses[expenses["description"].str.startswith(ZUS)]


def get_expenses_zus_total_per_year(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a total amount of ZUS payed yearly.
    """
    expenses = get_expense_data(db)
    all_zus_expense = expenses[expenses["description"].str.startswith(ZUS)]
    return get_yearly_totals(all_zus_expense).rename_axis("year")


def get_expenses_vat7(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of VAT-7 payments.
    """
    expenses = get_expense_data(db)
    return expenses[expenses["description"].str.contains(VAT_7)]


def get_expenses_vat7_total_per_year(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of VAT-7 payed yearly.
    """
    expenses = get_expense_data(db)
    all_vat7_expenses = expenses[expenses["description"].str.contains(VAT_7)]
    return get_yearly_totals(all_vat7_expenses).rename_axis("year")


def get_expenses_vat_ppe(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of VAT PPE payments.
    """
    expenses = get_expense_data(db)
    return expenses[expenses["description"].str.contains(VAT_PPE)]


def get_expenses_vat_ppe_total_per_year(db: pd.DataFrame):
    """
    For a given cleaned dataframe, return a dataframe with the total amount of VAT PPE payed yearly.
    """
    expenses = get_expense_data(db)
    all_vat_ppe_expenses = expenses[expenses["description"].str.contains(VAT_PPE)]
    return get_yearly_totals(all_vat_ppe_expenses).rename_axis("year")

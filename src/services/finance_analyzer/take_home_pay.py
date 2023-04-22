import pandas as pd
from services.finance_analyzer.process_data import get_expense_data, get_income_data


def get_take_home_pay_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the total amount of take_home_pay per month.
    """
    income_data = get_income_data(df)
    expense_data = get_expense_data(df)
    take_home_pay_monthly = income_monthly - expense_monthly
    take_home_pay_monthly = take_home_pay_monthly.rename(
        columns={"amount": "take_home_pay"}
    )
    return take_home_pay_monthly

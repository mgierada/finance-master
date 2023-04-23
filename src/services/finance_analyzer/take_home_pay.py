import pandas as pd
from services.finance_analyzer.process_data import (
    get_expense_data,
    get_income_data,
    get_monthly_totals,
)


def get_take_home_pay_monthly(df: pd.DataFrame) -> pd.DataFrame:
    """
    For a given cleaned dataframe, return a dataframe with the total amount of take_home_pay per month.
    """
    filter_list = ["ZAKŁAD", "VAT-7", "PPE"]
    filter_regex = "|".join(filter_list)
    income_data = get_income_data(df)
    expense_data = get_expense_data(df)
    all_const_exp = expense_data[expense_data["description"].str.contains(filter_regex)]
    income_monthly = get_monthly_totals(income_data)

    take_home_pay_monthly = pd.DataFrame()
    take_home_pay_monthly["take_home_pay"] = (
        income_monthly["amount"] + all_const_exp["amount"]
    )
    return take_home_pay_monthly

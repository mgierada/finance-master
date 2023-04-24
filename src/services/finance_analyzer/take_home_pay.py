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
    all_const_exp_monthly = get_monthly_totals(all_const_exp)
    income_monthly = get_monthly_totals(income_data)

    take_home_pay = pd.merge(
        all_const_exp_monthly, income_monthly, on="date", how="outer"
    )
    take_home_pay.rename(
        columns={"amount_x": "const_expenses", "amount_y": "income"}, inplace=True
    )
    take_home_pay.fillna(0, inplace=True)
    take_home_pay["take_home_pay"] = (
        take_home_pay["income"] + take_home_pay["const_expenses"]
    )
    return take_home_pay.sort_values(by="date", ascending=False)

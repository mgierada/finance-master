from services.finance_analyzer.constants import BASED_SALARY, MONTHLY_HOUR_MEAN
import typing as t


def get_ex_ante(overhours: int = 0) -> dict:
    """
    Calculate ex ante income and expenses for the end of current month.
    """
    return {
        "income": get_ex_ante_income(overhours),
    }


def get_ex_ante_income(overhours: int = 0) -> t.Dict[str, float]:
    """
    Calculate ex ante income for the end of current month.
    """
    overhours_income = overhours * (BASED_SALARY / MONTHLY_HOUR_MEAN)

    return {
        "based_income": BASED_SALARY,
        "overhours_income": overhours * (BASED_SALARY / MONTHLY_HOUR_MEAN),
        "total_income": overhours_income,
    }

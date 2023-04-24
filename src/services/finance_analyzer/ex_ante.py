from services.finance_analyzer.constants import BASED_SALARY, MONTHLY_HOUR_MEAN
import typing as t


def get_ex_ante(overhours: int = 0) -> dict:
    """
    Calculate ex ante income and expenses for the end of current month.
    """
    return {
        "income": get_ex_ante_income(overhours),
        "expenses": get_ex_ante_expenses(),
    }


def get_ex_ante_income(overhours: int = 0) -> t.Dict[str, float]:
    """
    Calculate ex ante income for the end of current month.
    """
    overhours_income = overhours * (BASED_SALARY / MONTHLY_HOUR_MEAN)
    based_income = get_based_income()
    overhours_income = get_overhours_income(overhours)
    total_income = get_total_income(based_income, overhours_income)

    return {
        "based_income": based_income,
        "overhours_income": overhours_income,
        "total_income": total_income,
    }


def get_based_income() -> int:
    """
    Calculate based income for the end of current month.
    """
    return BASED_SALARY


def get_overhours_income(overhours: int = 0) -> float:
    """
    Calculate overhours income for the end of current month.
    """
    return overhours * (BASED_SALARY / MONTHLY_HOUR_MEAN)


def get_total_income(based_income: int, overhours_income: float) -> float:
    return based_income + overhours_income


def get_ex_ante_expenses() -> t.Dict[str, float]:
    """
    Calculate ex ante expenses for the end of current month.
    """
    return {
        "const_expenses": 0,
        "var_expenses": 0,
        "total_expenses": 0,
    }

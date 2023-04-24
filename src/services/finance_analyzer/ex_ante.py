from services.finance_analyzer.constants import (
    BASED_SALARY,
    MONTHLY_HOUR_MEAN,
    ZUS_MONTHLY_EXPENSES,
)
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
    zus_expenses = get_ex_ante_zus_expenses()
    vat7_expenses = get_ex_ante_vat7_expenses()
    vat_ppe_expenses = get_ex_ante_vat_ppe_expenses()

    return {
        "zus_expenses": zus_expenses,
        "vat-7_expenses": vat7_expenses,
        "vat-ppe_expenses": vat_ppe_expenses,
    }


def get_ex_ante_zus_expenses() -> float:
    """
    Calculate ex ante ZUS expenses for the end of current month.
    """
    return ZUS_MONTHLY_EXPENSES


def get_ex_ante_vat7_expenses() -> float:
    """
    Calculate ex ante VAT-7 expenses for the end of current month.
    """
    return 0


def get_ex_ante_vat_ppe_expenses() -> float:
    """
    Calculate ex ante VAT-PPE expenses for the end of current month.
    """
    return 0

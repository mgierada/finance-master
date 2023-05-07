from services.finance_analyzer.constants import (
    BASED_SALARY,
    BONUS_EXPENSE,
    BONUS_INCOME,
    MONTHLY_HOUR_MEAN,
    ZUS_MONTHLY_EXPENSES,
)
import typing as t

from utils.utils import round_to_two_decimals_in_dict, round_to_two_decimals_in_float


def get_ex_ante(overhours: int = 0) -> t.Dict[str, float | t.Dict[str, float]]:
    """
    Calculate ex ante income and expenses for the end of current month.
    """
    ex_ante_income_summary = get_ex_ante_income_summary(overhours)
    ex_ante_expenses_summary = get_ex_ante_expenses_summary(
        ex_ante_income_summary["total_income"]
    )
    take_home_pay = (
        ex_ante_income_summary["total_income_vat_7_included"]
        + ex_ante_expenses_summary["total_expenses"]
    )
    return {
        "income": round_to_two_decimals_in_dict(ex_ante_income_summary),
        "expenses": round_to_two_decimals_in_dict(ex_ante_expenses_summary),
        "take-home-pay": round_to_two_decimals_in_float(take_home_pay),
    }


def get_ex_ante_income_summary(overhours: int = 0) -> t.Dict[str, float]:
    """
    Calculate ex ante income for the end of current month.
    """
    overhours_income = overhours * (BASED_SALARY / MONTHLY_HOUR_MEAN)
    based_income = get_based_income()
    bonus_income = get_bonus_income()
    overhours_income = get_overhours_income(overhours)
    total_income = get_total_income_or_expense(
        based_income, overhours_income, bonus_income
    )
    vat_7_income = get_vat_7_income_or_expenses(total_income)
    total_income_vat_7_included = total_income + vat_7_income

    return {
        "based_income": based_income,
        "overhours_income": overhours_income,
        "bonus_income": bonus_income,
        "total_income": total_income,
        "vat_7_income": vat_7_income,
        "total_income_vat_7_included": total_income_vat_7_included,
    }


def get_bonus_income() -> float:
    """
    Calculate bonus income for the end of current month.
    """
    return BONUS_INCOME


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


def get_total_income_or_expense(*args: float) -> float:
    return sum(args)


def get_ex_ante_expenses_summary(total_income: float) -> t.Dict[str, float]:
    """
    Calculate ex ante expenses for the end of current month.
    """
    zus_expenses = get_ex_ante_zus_expenses()
    vat7_expenses = get_vat_7_income_or_expenses(total_income) * -1
    vat_ppe_expenses = get_ex_ante_vat_ppe_expenses(total_income)
    bonus_expenses = get_bonus_expenses()
    total_expenses = get_total_income_or_expense(
        zus_expenses, vat7_expenses, vat_ppe_expenses, bonus_expenses
    )

    return {
        "zus_expenses": zus_expenses,
        "vat-7_expenses": vat7_expenses,
        "vat-ppe_expenses": vat_ppe_expenses,
        "total_expenses": total_expenses,
    }


def get_bonus_expenses() -> float:
    """
    Calculate bonus expenses for the end of current month.
    """
    return BONUS_EXPENSE


def get_ex_ante_zus_expenses() -> float:
    """
    Calculate ex ante ZUS expenses for the end of current month.
    """
    return ZUS_MONTHLY_EXPENSES


def get_vat_7_income_or_expenses(total_income: float) -> float:
    """
    Calculate ex ante VAT-7 expenses for the end of current month.
    """
    return 0.23 * total_income


def get_ex_ante_vat_ppe_expenses(total_income: float) -> float:
    """
    Calculate ex ante VAT-PPE expenses for the end of current month.
    """
    return -0.12 * total_income

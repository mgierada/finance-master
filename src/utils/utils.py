import typing as t


def filter_unwanted_fields_from_dict(
    dictionary: t.Dict[str, str], unwanted_fields: t.List[str]
):
    """
    Filter unwanted fields from a dictionary
    """
    return {
        key: value for key, value in dictionary.items() if key not in unwanted_fields
    }


def round_to_two_decimals_in_dict(
    dictionary: t.Dict[str, t.Union[int, float]]
) -> t.Dict[str, float]:
    """
    Round a number to two decimals
    """
    return {key: round(value, 2) for key, value in dictionary.items()}


def round_to_two_decimals_in_float(value: float) -> float:
    """
    Round a number to two decimals
    """
    return round(value, 2)

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

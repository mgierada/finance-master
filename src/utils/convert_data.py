from datetime import datetime


def convert_date(date_str: str) -> str:
    """Convert date string 2023-04-14T00:00:00.000 to date string 2023-04-14."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    return date_obj.strftime("%Y-%m-%d")

import calendar
from collections.abc import Callable
from datetime import datetime, date
from typing import Final

from app.definitions.input import Empty, Value
from app.services.transform.functions.general import handle_empties


EQ_DATETIME_FORMAT: Final[str] = "DD/MM/YYYY"
ISO_8601_FORMAT: Final[str] = "YYYY-MM-DD"
PCK_DATE_FORMAT: Final[str] = "DDMMYY"


def _get_date(text: str, format_str: str) -> date | bool:
    try:
        return datetime.strptime(text, format_str).date()
    except ValueError:
        return False


def _convert_to_datetime_format(format_str: str) -> str:
    return format_str.replace("DD", "%d").replace("MM", "%m").replace("YYYY", "%Y").replace("YY", "%y")


def _to_date(value: str, input_format: str, display_as: str, process: Callable[[date], date]) -> Value:
    input_f = _convert_to_datetime_format(input_format)
    if d := _get_date(value, input_f):
        d = process(d)
        format_str = _convert_to_datetime_format(display_as)
        return str(d.strftime(format_str))
    return Empty


@handle_empties
def to_date(value: str, input_format: str = EQ_DATETIME_FORMAT, display_as: str = PCK_DATE_FORMAT) -> Value:
    return _to_date(
        value,
        input_format=input_format,
        display_as=display_as,
        process=lambda d: d)


@handle_empties
def any_date(
            value: str,
            values: list[str] = [],
            input_format: str = EQ_DATETIME_FORMAT,
            on_true: str = "1",
            on_false: str = "2") -> str:

    all_values = [value] + values
    input_f = _convert_to_datetime_format(input_format)
    for val in all_values:
        if _get_date(val, input_f):
            return on_true
    return on_false


@handle_empties
def start_of_month(value: str, input_format: str = EQ_DATETIME_FORMAT, display_as: str = PCK_DATE_FORMAT) -> Value:
    return _to_date(
        value,
        input_format=input_format,
        display_as=display_as,
        process=lambda d: d.replace(day=1))


@handle_empties
def end_of_month(value: str, input_format: str = EQ_DATETIME_FORMAT, display_as: str = PCK_DATE_FORMAT) -> Value:
    return _to_date(
        value,
        input_format=input_format,
        display_as=display_as,
        process=lambda d: d.replace(day=calendar.monthrange(d.year, d.month)[1]))


@handle_empties
def start_of_year(value: str, input_format: str = EQ_DATETIME_FORMAT, display_as: str = PCK_DATE_FORMAT) -> Value:
    return _to_date(
        value,
        input_format=input_format,
        display_as=display_as,
        process=lambda d: d.replace(day=1, month=1))


@handle_empties
def end_of_year(value: str, input_format: str = EQ_DATETIME_FORMAT, display_as: str = PCK_DATE_FORMAT) -> Value:
    return _to_date(
        value,
        input_format=input_format,
        display_as=display_as,
        process=lambda d: d.replace(day=31, month=12))


@handle_empties
def month_year_string(value: str) -> Value:
    date_obj = datetime.strptime(value, '%Y%m')
    formatted_date = date_obj.strftime('%B %Y')
    return formatted_date


@handle_empties
def quarter_formatter(value: str) -> Value:
    """
    Converts a date string in YYYYMM format to a quarter string in Quarter 1/YYYY (January) format.
    """
    year = value[:4]
    month = value[-2]

    if month == "03":
        return f"Quarter 1/{year} ({calendar.month_name[1]})"
    elif month == "06":
        return f"Quarter 2/{year} ({calendar.month_name[4]})"
    elif month == "09":
        return f"Quarter 3/{year} ({calendar.month_name[7]})"
    elif month == "12":
        return f"Quarter 4/{year} ({calendar.month_name[10]})"

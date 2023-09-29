from app.definitions import Value, Empty
from app.transform.functions.numerical import round_half_up, divide
from app.transform.functions.time import to_date, ISO_8601_FORMAT, PCK_DATE_FORMAT, EQ_DATETIME_FORMAT


def currency_thousands(value: Value) -> Value:
    v = round_half_up(value, nearest="1000")
    val = divide(v, by="1000")
    return "0" if val == "-0" else val


def period_start(
        value: Value,
        period_start_date: str,
        period_input_format: str = ISO_8601_FORMAT,
        date_input_format: str = EQ_DATETIME_FORMAT,
        display_as: str = PCK_DATE_FORMAT) -> Value:

    if value is Empty:
        return to_date(period_start_date, input_format=period_input_format, display_as=display_as)
    else:
        return to_date(value, input_format=date_input_format, display_as=display_as)


def period_end(
        value: Value,
        period_end_date: str,
        period_input_format: str = ISO_8601_FORMAT,
        date_input_format: str = EQ_DATETIME_FORMAT,
        display_as: str = PCK_DATE_FORMAT) -> Value:

    if value is Empty:
        return to_date(period_end_date, input_format=period_input_format, display_as=display_as)
    else:
        return to_date(value, input_format=date_input_format, display_as=display_as)

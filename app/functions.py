from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import List
from datetime import datetime

from app.definitions import Value


def contains(
            value: Value,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    if value is None:
        return None
    if match_str in value:
        return on_true
    return on_false


def any_contains(
            value: Value,
            values: List[Value] = [],
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    all_values = [v for v in [value] + values if v is not None]
    if len(all_values) == 0:
        return None
    for val in all_values:
        if val is not None:
            if match_str in val:
                return on_true
    return on_false


def any_date(
            value: Value,
            values: List[Value] = [],
            on_true: str = "1",
            on_false: str = "2") -> Value:
    all_values = [v for v in [value] + values if v is not None]
    if len(all_values) == 0:
        return None
    for val in all_values:
        if val is not None:
            if _is_date(val):
                return on_true
    return on_false


def _is_date(text: str) -> bool:
    try:
        datetime.strptime(text, "%d/%m/%Y").date()
        return True
    except ValueError:
        return False


def exists(
        value: Value,
        on_true: str = "1",
        on_false: str = "2") -> Value:

    if value is not None:
        return on_true
    return on_false


def round_half_up(value: Value, precision: str) -> Value:

    if value is None:
        return None
    try:
        v = Decimal(value)
        p = Decimal(precision)
        return str(v.quantize(p, rounding=ROUND_HALF_UP))
    except InvalidOperation:
        return ""


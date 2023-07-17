from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import List
from datetime import datetime

from app.definitions import Value, Field


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
        if _is_date(val):
            return on_true
    return on_false


def _is_date(text: str) -> bool:
    try:
        datetime.strptime(text, "%d/%m/%Y").date()
        return True
    except ValueError:
        return False


def exists(value: Value, on_true: str = "1", on_false: str = "2") -> Value:
    if value is not None:
        return on_true
    return on_false


def any_exist(value: Value, values: list[Value], on_true: str = "1", on_false: str = "2") -> Value:
    if _all_nones(value, values):
        return on_false
    return on_true


def round_half_up(value: Value, nearest: str = "1") -> Value:
    v = _to_decimal(value, None)
    if v is None:
        return None

    p = _to_decimal(nearest, Decimal("1"))
    return str(Decimal(v / p).quantize(1, ROUND_HALF_UP) * p)


def aggregate(value: Value, values: list[Value], weight: str) -> Value:
    if _all_nones(value, values):
        return None

    w = _to_decimal(weight, Decimal(0))
    return str(_to_decimal(value) + sum(_to_decimal(val) * w for val in values))


def mean(value: Value, values: list[Value]) -> Value:
    if _all_nones(value, values):
        return None

    data = [_to_decimal(v) for v in [value] + values if v is not None]
    divisor = len(data)
    return str(sum(data) / divisor)


def concat(value: Value, values: list[Value], seperator: str = " ") -> Value:
    if _all_nones(value, values):
        return None

    return seperator.join([v for v in [value] + values if v is not None])


def _to_decimal(value: Value, default: Decimal | None = Decimal(0)) -> Decimal:
    if value is None:
        return default
    try:
        return Decimal(value)
    except InvalidOperation:
        return default


def _all_nones(*fields: Field) -> bool:
    for f in fields:
        if isinstance(f, dict):
            for x in f.values():
                if x is not None:
                    return False
        if isinstance(f, list):
            for x in f:
                if x is not None:
                    return False
        else:
            if f is not None:
                return False
    return True

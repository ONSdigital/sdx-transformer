from decimal import Decimal, ROUND_HALF_UP

from app.definitions import Value, Empty
from app.functions.common import all_non_decimal

"""
This file contains the functions that represent
the transformations that can be performed on string
arguments that represent numerical values
within a build spec.
"""


@all_non_decimal
def round_half_up(value: Value, nearest: str = "1") -> Value:
    v = _to_decimal(value)
    p = _to_decimal(nearest, Decimal("1"))
    return str(Decimal(v / p).quantize(1, ROUND_HALF_UP) * p)


@all_non_decimal
def aggregate(value: Value, values: list[Value], weight: str) -> Value:
    w = _to_decimal(weight, Decimal(0))
    return str(_to_decimal(value) + sum(_to_decimal(val) * w for val in values))


@all_non_decimal
def mean(value: Value, values: list[Value]) -> Value:
    data = [_to_decimal(v) for v in [value] + values if v is not Empty]
    divisor = len(data)
    return str(sum(data) / divisor)


@all_non_decimal
def number_equals(value: Value, comparand: str = "", on_true: str = "1", on_false: str = "2") -> Value:
    v = _to_decimal(value)
    c = _to_decimal(comparand, Empty)

    if c is Empty:
        return Empty

    if v == c:
        return on_true
    return on_false


def _to_decimal(value: Value, default: Decimal | Empty = Decimal(0)) -> Decimal:
    if value is Empty:
        return default
    try:
        return Decimal(value)
    except Exception:
        return default

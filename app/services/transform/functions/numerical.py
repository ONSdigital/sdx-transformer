from collections.abc import Callable
from decimal import Decimal, ROUND_HALF_UP

from app.definitions.input import Empty, Value

"""
This file contains the functions that represent
the transformations that can be performed on string
arguments that represent numerical values
within a build spec.
"""


def _to_decimal(value: Value, default: Decimal | Empty = Empty) -> Decimal:
    if value is Empty:
        return default
    try:
        return Decimal(value)
    except Exception:
        return default


def all_decimals(func: Callable[..., Value]) -> Callable[..., Value]:
    def inner(value: Value, **kwargs: Value):
        found_decimal = False

        if "values" in kwargs:
            values = [
                val for val in [_to_decimal(v) for v in kwargs["values"]]
                if val is not Empty
            ]
            if len(values) > 0:
                found_decimal = True
            kwargs["values"] = values

        v = _to_decimal(value)
        if v is not Empty:
            found_decimal = True
        else:
            if found_decimal:
                v = Decimal("0")

        if found_decimal:
            return str(func(v, **kwargs))
        else:
            return Empty

    return inner


@all_decimals
def round_half_up(value: Decimal, nearest: str = "1") -> Decimal:
    p = _to_decimal(nearest, Decimal("1"))
    return Decimal(value / p).quantize(1, ROUND_HALF_UP) * p


@all_decimals
def total(value: Decimal, values: list[Decimal]) -> Decimal:
    return sum([value] + values)


@all_decimals
def divide(value: Decimal, by: str = "1") -> Decimal:
    d = _to_decimal(by)
    if d is Empty or d == 0:
        return Empty
    return value / d


@all_decimals
def aggregate(value: Decimal, values: list[Decimal], weight: str) -> Decimal:
    w = _to_decimal(weight, Decimal("0"))
    return value + sum(val * w for val in values)


@all_decimals
def mean(value: Decimal, values: list[Decimal]) -> Decimal:
    data = [value] + values
    divisor = len(data)
    return sum(data) / divisor


@all_decimals
def number_equals(
        value: Decimal,
        comparand: str = "",
        on_true: str = "1",
        on_false: str = "2") -> Value:

    c = _to_decimal(comparand, Empty)

    if c is Empty:
        return Empty

    if value == c:
        return on_true
    return on_false

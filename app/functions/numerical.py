from decimal import Decimal, ROUND_HALF_UP

from app.definitions import Value, Empty
from app.functions.common import _all_empty


def round_half_up(value: Value, nearest: str = "1") -> Value:
    v = _to_decimal(value, Empty)
    if v is Empty:
        return Empty

    p = _to_decimal(nearest, Decimal("1"))
    return str(Decimal(v / p).quantize(1, ROUND_HALF_UP) * p)


def aggregate(value: Value, values: list[Value], weight: str) -> Value:
    if _all_empty(value, values):
        return Empty

    w = _to_decimal(weight, Decimal(0))
    return str(_to_decimal(value) + sum(_to_decimal(val) * w for val in values))


def mean(value: Value, values: list[Value]) -> Value:
    if _all_empty(value, values):
        return Empty

    data = [_to_decimal(v) for v in [value] + values if v is not Empty]
    divisor = len(data)
    return str(sum(data) / divisor)


def number_equals(value: Value, comparand: str = "", on_true: str = "1", on_false: str = "2") -> Value:
    v = _to_decimal(value, Empty)
    c = _to_decimal(comparand, Empty)

    if v is Empty or c is Empty:
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

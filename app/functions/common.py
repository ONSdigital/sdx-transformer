from collections.abc import Callable
from decimal import Decimal

from app.definitions import Empty, Value


def all_empty(func: Callable[..., Value]) -> Callable[..., Value]:
    def inner(value: Value, **kwargs: Value):
        non_empty = False
        if value is not Empty:
            non_empty = True
        elif "values" in kwargs:
            for v in kwargs["values"]:
                if v is not Empty:
                    non_empty = True

        if non_empty:
            return func(value, **kwargs)
        else:
            return Empty

    return inner


def all_non_decimal(func: Callable[..., Value]) -> Callable[..., Value]:
    def inner(value: Value, **kwargs: Value):
        found_decimal = False
        if _is_decimal(value):
            found_decimal = True
        elif "values" in kwargs:
            for v in kwargs["values"]:
                if _is_decimal(v):
                    found_decimal = True

        if found_decimal:
            return func(value, **kwargs)
        else:
            return Empty

    return inner


def _is_decimal(value: Value) -> bool:
    if value is Empty:
        return False
    try:
        _d = Decimal(value)  # noqa: F841
        return True
    except Exception:
        return False

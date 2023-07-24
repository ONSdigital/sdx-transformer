from typing import List
from datetime import datetime

from app.definitions import Value, Empty
from app.functions.common import _all_empty

"""
This file contains the functions that represent
the transformations that can be performed on string
arguments within a build spec.
"""


def contains(
            value: Value,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    if value is Empty:
        return Empty
    if match_str in value:
        return on_true
    return on_false


def any_contains(
            value: Value,
            values: List[Value] = [],
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    all_values = [v for v in [value] + values if v is not Empty]
    if len(all_values) == 0:
        return Empty
    for val in all_values:
        if val is not Empty:
            if match_str in val:
                return on_true
    return on_false


def to_date(value: Value) -> Value:
    if value is Empty:
        return Empty
    if _is_date(value):
        d = datetime.strptime(value, "%d/%m/%Y").date()
        return str(int(d.strftime('%d%m%y')))
    return Empty


def any_date(
            value: Value,
            values: List[Value] = [],
            on_true: str = "1",
            on_false: str = "2") -> Value:
    all_values = [v for v in [value] + values if v is not Empty]
    if len(all_values) == 0:
        return Empty
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
    if value is not Empty:
        return on_true
    return on_false


def any_exists(value: Value, values: list[Value], on_true: str = "1", on_false: str = "2") -> Value:
    if _all_empty(value, values):
        return on_false
    return on_true


def concat(value: Value, values: list[Value], seperator: str = " ") -> Value:
    if _all_empty(value, values):
        return Empty

    return seperator.join([v for v in [value] + values if v is not Empty and v != ""])

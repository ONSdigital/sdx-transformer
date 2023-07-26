from typing import List
from datetime import datetime

from app.definitions import Value, Empty
from app.functions.common import all_empty

"""
This file contains the functions that represent
the transformations that can be performed on string
arguments within a build spec.
"""


def no_transform(value: Value) -> Value:
    return value


@all_empty
def starts_with(
            value: Value,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    if value.startswith(match_str):
        return on_true
    return on_false


@all_empty
def contains(
            value: Value,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    if match_str in value:
        return on_true
    return on_false


@all_empty
def any_contains(
            value: Value,
            values: List[Value] = [],
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> Value:

    all_values = [v for v in [value] + values if v is not Empty]
    for val in all_values:
        if match_str in val:
            return on_true
    return on_false


@all_empty
def to_date(value: Value, display_as: str = "%d%m%y") -> Value:
    if _is_date(value):
        d = datetime.strptime(value, "%d/%m/%Y").date()
        return str(int(d.strftime(display_as)))
    return Empty


@all_empty
def any_date(
            value: Value,
            values: List[Value] = [],
            on_true: str = "1",
            on_false: str = "2") -> Value:

    all_values = [v for v in [value] + values if v is not Empty]
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
    if value is not Empty:
        return on_true
    for v in values:
        if v is not Empty:
            return on_true
    return on_false


@all_empty
def concat(value: Value, values: list[Value], seperator: str = " ") -> Value:
    return seperator.join([v for v in [value] + values if v is not Empty and v != ""])

from collections.abc import Callable
from typing import Final
from datetime import datetime

from app.definitions import Value, Empty

"""
This file contains the functions that represent
the transformations that can be performed on string
values within a build spec.
"""

CURRENT_VALUE_IDENTIFIER: Final = "&value"


def all_string(func: Callable[..., Value]) -> Callable[..., Value]:
    def inner(value: Value, **kwargs: Value):
        found_str = False

        if "values" in kwargs:
            values = [v for v in kwargs["values"] if v is not Empty]
            if len(values) > 0:
                found_str = True
            kwargs["values"] = values

        v = value
        if v is not Empty:
            found_str = True
        else:
            if found_str:
                v = ""

        if found_str:
            return func(v, **kwargs)
        else:
            return Empty

    return inner


def no_transform(value: Value) -> Value:
    return value


@all_string
def starts_with(
            value: str,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> str:

    if value.startswith(match_str):
        return on_true
    return on_false


@all_string
def contains(
            value: str,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> str:

    if match_str in value:
        return on_true
    return on_false


@all_string
def any_contains(
            value: str,
            values: list[str] = [],
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> str:

    all_values = [value] + values
    for val in all_values:
        if match_str in val:
            return on_true
    return on_false


@all_string
def to_date(value: str, display_as: str = "%d%m%y") -> Value:
    if _is_date(value):
        d = datetime.strptime(value, "%d/%m/%Y").date()
        return str(int(d.strftime(display_as)))
    return Empty


@all_string
def any_date(
            value: str,
            values: list[str] = [],
            on_true: str = "1",
            on_false: str = "2") -> str:

    all_values = [value] + values
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
    if value is not Empty and value != "":
        return on_true
    return on_false


def any_exists(value: Value, values: list[Value], on_true: str = "1", on_false: str = "2") -> Value:
    if value is not Empty and value != "":
        return on_true
    for v in values:
        if v is not Empty and value != "":
            return on_true
    return on_false


@all_string
def concat(value: str, values: list[str], seperator: str = " ") -> Value:
    return seperator.join([v for v in [value] + values if v != ""])

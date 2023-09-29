from app.definitions import Value
from app.transform.functions.general import handle_empties

"""
This file contains the functions that represent
the transformations that can be performed on string
values within a build spec.
"""


@handle_empties
def starts_with(
            value: str,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> str:

    if value.startswith(match_str):
        return on_true
    return on_false


@handle_empties
def contains(
            value: str,
            match_str: str = "",
            on_true: str = "1",
            on_false: str = "2") -> str:

    if match_str in value:
        return on_true
    return on_false


@handle_empties
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


@handle_empties
def concat(value: str, values: list[str], seperator: str = " ") -> Value:
    return seperator.join([v for v in [value] + values if v != ""])

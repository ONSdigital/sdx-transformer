import math
import re

from app.definitions.data import Value
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


@handle_empties
def carve(value: str, start_index=0, end_index=None) -> Value:
    """
    Could not be named slice, as this is a keyword
    """

    # No params, just split in half
    if start_index == 0 and not end_index:
        return value[:math.floor(len(value)/2)]

    # End index will default to end of string
    elif not end_index:
        return value[start_index:]

    return value[start_index:end_index]


@handle_empties
def string_padding(value: Value, padding_length: str) -> Value:
    return value.ljust(int(padding_length))


@handle_empties
def space_split(value: str, index: int = 0) -> Value:
    """
    Will split a string based on a space and return the part as denoted by the index.
    If the index is not valid then the un transformed value will be returned.
    :param value The data
    :param index The index of the data to return, 0 = first part, 1 = second part etc
    """

    # Strip out any tabs and double spaces etc
    cleaned = re.sub(r"\s+", " ", value)
    parts = cleaned.split(" ")
    if len(parts) > index:
        return parts[index]
    return value


def postcode(value: str) -> tuple[str, str]:
    parts = value.split(" ")
    if len(parts) > 1:
        return parts[0], parts[1]

    x = len(value) - 3
    return value[:x], value[x:]


@handle_empties
def postcode_start(value: str) -> Value:
    return postcode(value)[0]


@handle_empties
def postcode_end(value: str) -> Value:
    return postcode(value)[1]

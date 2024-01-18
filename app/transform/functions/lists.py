from app.definitions import Value, Empty

"""
This file contains the functions that represent
transformations within a build spec that result in a list.
"""


def as_list(_value: Value, values: list[Value]) -> list[Value]:
    return [v if v is not Empty else "" for v in values]


def append_to_list(value: Value, values: list[Value]) -> list[Value]:
    full = values + [value]
    return as_list("", values=full)


def prepend_to_list(value: Value, values: list[Value]) -> list[Value]:
    full = [value] + values
    return as_list("", values=full)


def trim_list(_value: Value, values: list[Value]) -> list[Value]:
    return [v for v in values if v is not Empty]

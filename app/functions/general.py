from typing import Callable

from app.definitions import Value, Empty

"""
This file contains the functions that represent
general transformations within a build spec.
"""


def no_transform(value: Value) -> Value:
    return value


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


def handle_empties(func: Callable[..., Value]) -> Callable[..., Value]:
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

import unittest
from collections.abc import Callable

import app.execute
from app.definitions import ParseTree
from app.execute import execute


def fake_remove_chars(value: str, n: str = "1") -> str:
    return value[int(n):]


def fake_add(value: str, values: list[str] = []) -> str:
    return str(sum([int(x) for x in (values + [value])]))


def fake_contains(value: str, match_str: str = "", on_true: str = "1", on_false: str = "2") -> str:
    if match_str in value:
        return on_true
    return on_false


class ExecutionTests(unittest.TestCase):

    def setUp(self) -> None:
        fake_function_lookup: dict[str, Callable] = {
            "REMOVE_CHARS": fake_remove_chars,
            "ADD": fake_add,
            "CONTAINS": fake_contains
        }
        app.execute._function_lookup = fake_function_lookup

    def test_execute_single(self):

        parse_tree: ParseTree = {
            "150": {
                "name": "REMOVE_CHARS",
                "args": {
                    "value": "hello",
                    "n": "2",
                }
            }
        }

        expected = {
            "150": "llo",
        }

        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

    def test_execute_nested(self):

        parse_tree: ParseTree = {
            "150": "10",
            "151": None,
            "152": {
                "name": "REMOVE_CHARS",
                "args": {
                    "value": "hello",
                    "n": "1",
                }
            },
            "153": {
                "name": "REMOVE_CHARS",
                "args": {
                    "value": {
                        "name": "REMOVE_CHARS",
                        "args": {
                            "value": {
                                "name": "REMOVE_CHARS",
                                "args": {
                                    "n": "1",
                                    "value": "abcdefgh"
                                },
                            },
                            "n": "2",
                        }
                    },
                    "n": "3",
                }
            },
            "154": {
                "name": "ADD",
                "args": {
                    "value": "5",
                    "values": ["6", "7"]
                },
            },
            "156": {
                "name": "ADD",
                "args": {
                    "value": "100",
                    "values": ["200", "300", "400"]
                },
            }
        }

        expected = {
            "150": "10",
            "151": None,
            "152": "ello",
            "153": "gh",
            "154": "18",
            "156": "1000",
        }
        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

    def test_execute_transform_in_args(self):

        parse_tree: ParseTree = {
            "152": {
                "name": "ADD",
                "args": {
                    "value": "100",
                    "values": [
                        "200",
                        "300",
                        {
                            "name": "REMOVE_CHARS",
                            "args": {
                                "n": "1",
                                "value": "a400"
                            },
                        },
                    ]
                },
            }
        }

        expected = {
            "152": "1000"
        }
        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

    def test_execute_derived(self):

        parse_tree: ParseTree = {
            "150": {
                "name": "REMOVE_CHARS",
                "args": {
                    "value": "hello",
                    "n": "2",
                }
            },
            "151": "&150"
        }

        expected = {
            "150": "llo",
            "151": "llo"
        }

        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

    def test_execute_nested_derived(self):

        parse_tree: ParseTree = {
            "150": "100",
            "151": {
                "name": "ADD",
                "args": {
                    "value": "0",
                    "values": ["&150", "2", "3"]
                }
            },
            "152": {
                "name": "REMOVE_CHARS",
                "args": {
                    "value": {
                        "name": "ADD",
                        "args": {
                            "value": "0",
                            "values": ["&150", "&151"]
                        }
                    },
                    "n": "2",
                }
            },
        }

        expected = {
            "150": "100",
            "151": "105",
            "152": "5"
        }

        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

    def test_execute_nested_derived_current(self):

        parse_tree: ParseTree = {
            "152": {
                "name": "CONTAINS",
                "args": {
                    "value": {
                        "name": "REMOVE_CHARS",
                        "args": {
                            "value": "hat",
                            "n": "1",
                        }
                    },
                    "match_str": "at",
                    "on_true": "&value",
                    "on_false": "not found!"
                }
            },
        }

        expected = {
            "152": "at"
        }

        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

import unittest
from collections.abc import Callable

from app.definitions import ParseTree
from app.execute import execute, set_lookups


def fake_remove_chars(value: str, n: str = "1") -> str:
    return value[int(n):]


def fake_add(value: str, values: list[str] = []) -> str:
    return str(sum([int(x) for x in (values + [value])]))


class ExecutionTests(unittest.TestCase):

    def setUp(self) -> None:
        fake_function_lookup: dict[str, Callable] = {
            "REMOVE_CHARS": fake_remove_chars,
            "ADD": fake_add
        }
        set_lookups(fake_function_lookup)

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

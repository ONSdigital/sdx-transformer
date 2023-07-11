import unittest

from app.definitions import ParseTree
from app.execute import execute, Function


class FakeRemoveChars(Function):

    def perform(self, value: str, n: str = "1") -> str:
        return value[int(n):]


class FakeAdd(Function):

    def perform(self, value: str, values: list[str] = []) -> str:
        return str(sum([int(x) for x in (values + [value])]))


class ExecutionTests(unittest.TestCase):

    def setUp(self) -> None:
        function_lookup: dict[str, Function.__class__] = {
            "REMOVE_CHARS": FakeRemoveChars,
            "ADD": FakeAdd
        }
        Function.set_function_lookup(function_lookup)

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

import unittest

from app.definitions import ParseTree
from app.execute import execute


class ExecutionTests(unittest.TestCase):

    def test_execute(self):

        parse_tree: ParseTree = {
            "150": {
                "name": "ROUND",
                "args": {
                    "value": "1.2",
                    "precision": "1",
                }
            }
        }

        expected = {
            "150": "1",
        }

        actual = execute(parse_tree)
        self.assertEqual(expected, actual)

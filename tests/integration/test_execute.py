import unittest

from app.definitions import Template, Transforms
from app.execute import execute


class ExecuteTests(unittest.TestCase):

    def test1(self):

        data = {
            "151": "56.7"
        }

        template: Template = {
            "151": "$ROUND"
        }

        transforms: Transforms = {
            "$ROUND": {
                "name": "ROUND",
                "args": {
                    "value": "#151",
                    "precision": "1",
                    "direction": "ROUND_HALF_UP"
                }
            }
        }

        expected = {"151": "57"}
        actual = execute(data, template, transforms)
        self.assertEqual(expected, actual)

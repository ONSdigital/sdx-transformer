import unittest

from app.definitions import Template
from app.transform.clean import clean


class CleanTests(unittest.TestCase):

    def test_remove_empty_from_list(self):

        input_data: Template = {
            "address": [
                "56 Random Lane",
                "Turtleland",
                "",
                "",
                "",
                "RU67B52"
            ],
        }

        actual = clean(input_data)
        expected = {
            "address": [
                "56 Random Lane",
                "Turtleland",
                "RU67B52"
            ],
        }
        self.assertEqual(expected, actual)

    def test_remove_empty_from_not_at_top_level(self):

        input_data: Template = {
            "company": {
                "name": "My company",
                "address": [
                    "56 Random Lane",
                    "Turtleland",
                    "",
                    "",
                    "",
                    "RU67B52"
                ],
            }

        }

        actual = clean(input_data)
        expected = {
            "company": {
                "name": "My company",
                "address": [
                    "56 Random Lane",
                    "Turtleland",
                    "RU67B52"
                ],
            }

        }
        self.assertEqual(expected, actual)

    def test_remove_empty_from_nested_list(self):

        input_data: Template = {
            "addresses": [
                [
                    "56 Random Lane",
                    "Turtleland",
                    "",
                    "",
                    "",
                    "RU67B52"
                ],
                [],
                [
                    ""
                    ""
                ]
            ],

        }

        actual = clean(input_data)
        expected = {
            "addresses": [
                [
                    "56 Random Lane",
                    "Turtleland",
                    "RU67B52"
                ]
            ],

        }
        self.assertEqual(expected, actual)

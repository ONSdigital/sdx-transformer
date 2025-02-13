import unittest

from app.definitions.spec import Template
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

    def test_remove_parent_if_no_children(self):

        input_data: Template = {
            "company": {
                "name": "My company",
                "address": [
                    "",
                    "",
                    "",
                ],
            }

        }

        actual = clean(input_data)
        expected = {
            "company": {
                "name": "My company",
            }

        }
        self.assertEqual(expected, actual)

    def test_remove_field_from_object(self):

        input_data: Template = {
            "company": {
                "name": "My company",
                "vat": {
                    "thing1": "",
                    "thing2": "123"
                }
            }

        }

        actual = clean(input_data)
        expected = {
            "company": {
                "name": "My company",
                "vat": {
                    "thing2": "123"
                }
            }

        }
        self.assertEqual(expected, actual)

    def test_remove_whole_object_empty(self):

        input_data: Template = {
            "company": {
                "name": "My company",
                "vat": {
                    "thing1": "",
                    "thing2": ""
                }
            }

        }

        actual = clean(input_data)
        expected = {
            "company": {
                "name": "My company",
            }

        }
        self.assertEqual(expected, actual)

    def test_remove_top_level_key(self):

        input_data: Template = {
            "company": {
                "name": "",
                "vat": {
                    "thing1": "",
                    "thing2": ""
                }
            },
            "pet": "cat"

        }

        actual = clean(input_data)
        expected = {
            "pet": "cat"
        }
        self.assertEqual(expected, actual)

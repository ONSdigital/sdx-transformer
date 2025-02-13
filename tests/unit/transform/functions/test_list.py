import unittest

from app.definitions.data import Empty
from app.transform.functions.lists import as_list, append_to_list, prepend_to_list, trim_list


class ListTests(unittest.TestCase):

    def test_as_list(self):
        value = "foo"
        values = ["a", Empty, "c"]
        actual = as_list(value, values=values)
        expected = ["a", "", "c"]
        self.assertEqual(expected, actual)

    def test_append_to_list(self):
        value = "foo"
        values = ["a", Empty, "c"]
        actual = append_to_list(value, values=values)
        expected = ["a", "", "c", "foo"]
        self.assertEqual(expected, actual)

    def test_prepend_to_list(self):
        value = "foo"
        values = ["a", Empty, "c"]
        actual = prepend_to_list(value, values=values)
        expected = ["foo", "a", "", "c"]
        self.assertEqual(expected, actual)

    def test_trim_list(self):
        value = "foo"
        values = ["a", Empty, "c"]
        actual = trim_list(value, values=values)
        expected = ["a", "c"]
        self.assertEqual(expected, actual)

    def test_trim_list_all_empty(self):
        value = "foo"
        values = [Empty, Empty, Empty]
        actual = trim_list(value, values=values)
        expected = []
        self.assertEqual(expected, actual)

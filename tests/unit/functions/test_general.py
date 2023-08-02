import unittest

from app.definitions import Empty
from app.functions.general import exists, any_exists


class ExistsTests(unittest.TestCase):

    def test_true(self):
        value = "foo"
        actual = exists(value, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = None
        actual = exists(value, on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)


class AnyExistTests(unittest.TestCase):

    def test_true(self):
        value = "foo"
        values = [Empty, Empty]
        actual = any_exists(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = Empty
        values = [Empty, Empty]
        actual = any_exists(value, values=values, on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)

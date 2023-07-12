import unittest
from app.functions import Contains, Exists


class MatchesTests(unittest.TestCase):
    def test_true(self):
        value = "sentence for testing purposes"
        args = {"match_str": "testing", "on_true": "1", "on_false": "2"}
        contains = Contains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = "sentence for testing purposes"
        args = {"match_str": "I don't exist", "on_true": "1", "on_false": "2"}
        contains = Contains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "2"
        self.assertEqual(expected, actual)


class ExistsTests(unittest.TestCase):
    def test_true(self):
        value = "foo"
        args = {"on_true": "1", "on_false": "2"}
        exists = Exists(value=value, args=args)
        actual = exists.perform(value, **args)
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = None
        args = {"on_true": "1", "on_false": "2"}
        exists = Exists(value=value, args=args)
        actual = exists.perform(value, **args)
        expected = "2"
        self.assertEqual(expected, actual)


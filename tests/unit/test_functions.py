import unittest
from app.functions import Contains, Exists, AnyContains


class ContainsTests(unittest.TestCase):
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

    def test_none(self):
        value = None
        args = {"match_str": "I don't exist", "on_true": "1", "on_false": "2"}
        contains = Contains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = None
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


class AnyContainsTests(unittest.TestCase):
    def test_true(self):
        value = "sentence for testing purposes"
        values = []
        args = {"values": values, "match_str": "testing", "on_true": "1", "on_false": "2"}
        contains = AnyContains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "1"
        self.assertEqual(expected, actual)

    def test_true_list(self):
        value = "sometimes"
        values = ["yes", "no"]
        args = {"values": values, "match_str": "y", "on_true": "1", "on_false": "2"}
        contains = AnyContains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "1"
        self.assertEqual(expected, actual)

    def test_nones(self):
        value = None
        values = ["yes", "no", None]
        args = {"values": values, "match_str": "y", "on_true": "1", "on_false": "2"}
        contains = AnyContains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "1"
        self.assertEqual(expected, actual)

    def test_all_nones(self):
        value = None
        values = [None, None, None]
        args = {"values": values, "match_str": "y", "on_true": "1", "on_false": "2"}
        contains = AnyContains(value=value, args=args)
        actual = contains.perform(value, **args)
        expected = "2"
        self.assertEqual(expected, actual)

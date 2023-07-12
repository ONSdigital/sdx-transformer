import unittest
from app.functions import Matches


class MatchesTests(unittest.TestCase):
    def test_contains_true(self):
        value = "sentence for testing purposes"
        args = {"match_str": "testing", "match_type": "contains", "on_true": "1", "on_false": "2"}
        match = Matches(value=value, args=args)
        actual = match.apply()
        expected = "1"
        self.assertEqual(expected, actual)

    def test_contains_false(self):
        value = "sentence for testing purposes"
        args = {"match_str": "I don't exist", "match_type": "contains", "on_true": "1", "on_false": "2"}
        match = Matches(value=value, args=args)
        actual = match.apply()
        expected = "2"
        self.assertEqual(expected, actual)


class ExistsTests(unittest.TestCase):
    pass


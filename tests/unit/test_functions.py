import unittest

from app.functions import contains, any_contains, any_date, exists, round_half_up


class ContainsTests(unittest.TestCase):

    def test_true(self):
        value = "sentence for testing purposes"
        actual = contains(value, match_str="testing", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = "sentence for testing purposes"
        actual = contains(value, match_str="I don't exist", on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)

    def test_none_returns_none(self):
        value = None
        actual = contains(value, match_str="I don't exist", on_true="1", on_false="2")
        expected = None
        self.assertEqual(expected, actual)


class AnyContainsTests(unittest.TestCase):

    def test_true(self):
        value = "sentence for testing purposes"
        values = []
        actual = any_contains(value, values=values, match_str="testing", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_true_list(self):
        value = "sometimes"
        values = ["yes", "no"]
        actual = any_contains(value, values=values, match_str="y", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_none_doesnt_fail(self):
        value = None
        values = ["yes", "no", None]
        actual = any_contains(value, values=values, match_str="y", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_all_nones_returns_none(self):
        value = None
        values = [None, None, None]
        actual = any_contains(value, values=values, match_str="y", on_true="1", on_false="2")
        expected = None
        self.assertEqual(expected, actual)


class AnyDateTests(unittest.TestCase):

    def test_true(self):
        value = "12/07/2023"
        values = []
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_invalid_date_returns_on_false(self):
        value = "12/13/2023"
        values = []
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)

    def test_true_for_date_in_list(self):
        value = ""
        values = ["12/07/2023", "13/07/2023"]
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_some_nones_dont_fail(self):
        value = "12/07/2023"
        values = [None, None]
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_all_nones_returns_none(self):
        value = None
        values = [None, None, None]
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = None
        self.assertEqual(expected, actual)


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


class RoundTests(unittest.TestCase):

    def test_none_returns_none(self):
        value = None
        actual = round_half_up(value, precision="")
        expected = None
        self.assertEqual(expected, actual)

    def test_none_numerical_val_returns_empty_str(self):
        value = "I'm NaN"
        actual = round_half_up(value, precision="")
        expected = ""
        self.assertEqual(expected, actual)

    def test_rounds_two_point_nine_to_three(self):
        value = "2.9"
        precision = "1"
        actual = round_half_up(value, precision=precision)
        expected = "3"
        self.assertEqual(expected, actual)

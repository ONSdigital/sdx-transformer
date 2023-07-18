import unittest

from app.definitions import Empty
from app.functions.numerical import round_half_up, aggregate, mean, number_equals


class RoundTests(unittest.TestCase):

    def test_none_returns_none(self):
        value = None
        actual = round_half_up(value, nearest="")
        expected = None
        self.assertEqual(expected, actual)

    def test_none_numerical_val_returns_none(self):
        value = "I'm NaN"
        actual = round_half_up(value, nearest="")
        expected = None
        self.assertEqual(expected, actual)

    def test_rounding_to_nearest_1000(self):
        tests = {
            "3": "0",
            "78": "0",
            "499": "0",
            "500": "1000",
            "1306": "1000",
            "1500": "2000",
            "7805": "8000",
            "357899": "358000",
            "4999999": "5000000"
        }
        for value, expected in tests.items():
            actual = round_half_up(value, nearest="1000")
            self.assertEqual(expected, actual, f"{value} should have rounded to {expected}")

    def test_rounding_to_2dp(self):
        tests = {
            "3.245": "3.25",
            "0.1111": "0.11",
            "4.999999": "5.00"
        }
        for value, expected in tests.items():
            actual = round_half_up(value, nearest="0.01")
            self.assertEqual(expected, actual, f"{value} should have rounded to {expected}")


class AggregateTests(unittest.TestCase):

    def test_simple(self):
        value = "5"
        values = ["1", "2"]
        weight = "0.5"
        actual = aggregate(value, values=values, weight=weight)
        expected = "6.5"
        self.assertEqual(expected, actual)

    def test_none_value_doest_fail(self):
        value = None
        values = ["1", "2"]
        weight = "0.5"
        actual = aggregate(value, values=values, weight=weight)
        expected = "1.5"
        self.assertEqual(expected, actual)

    def test_none_values_doest_fail(self):
        value = None
        values = [None, "2"]
        weight = "1"
        actual = aggregate(value, values=values, weight=weight)
        expected = "2"
        self.assertEqual(expected, actual)

    def test_all_nones_returns_none(self):
        value = None
        values = [None, None]
        weight = "0.5"
        actual = aggregate(value, values=values, weight=weight)
        expected = None
        self.assertEqual(expected, actual)


class MeanTests(unittest.TestCase):

    def test_all_nones_returns_none(self):
        value = None
        values = [None, None]
        actual = mean(value, values=values)
        expected = None
        self.assertEqual(expected, actual)

    def test_simple(self):
        value = "3"
        values = ["4", "5"]
        actual = mean(value, values=values)
        expected = "4"
        self.assertEqual(expected, actual)


class NumberEqualTests(unittest.TestCase):

    def test_empty_returns_empty(self):
        value = Empty
        actual = number_equals(value, comparand="")
        expected = Empty
        self.assertEqual(expected, actual)

    def test_number_equals_true(self):
        value = "5.0"
        actual = number_equals(value, comparand="5", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_number_equals_false(self):
        value = "5.01"
        actual = number_equals(value, comparand="5", on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)

    def test_number_equals_false_negative(self):
        value = "-5"
        actual = number_equals(value, comparand="5", on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)

    def test_blank_returns_empty(self):
        value = ""
        actual = number_equals(value, comparand="5")
        expected = Empty
        self.assertEqual(expected, actual)

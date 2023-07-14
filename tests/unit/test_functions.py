import unittest

from app.functions import contains, any_contains, any_date, exists, round_half_up, aggregate, mean, concat


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


class ConcatTests(unittest.TestCase):

    def test_all_nones_returns_none(self):
        value = None
        values = [None, None]
        actual = concat(value, values=values)
        expected = None
        self.assertEqual(expected, actual)

    def test_simple(self):
        value = "a"
        values = ["b", "c"]
        actual = concat(value, values=values, seperator="-")
        expected = "a-b-c"
        self.assertEqual(expected, actual)

    def test_no_fail_on_none(self):
        value = "a"
        values = [None, "c"]
        actual = concat(value, values=values, seperator="_")
        expected = "a_c"
        self.assertEqual(expected, actual)

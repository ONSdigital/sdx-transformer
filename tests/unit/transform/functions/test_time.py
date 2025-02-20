import unittest

from app.definitions.input import Empty
from app.services.transform.functions.time import any_date, to_date, start_of_month, end_of_month


class ToDateTests(unittest.TestCase):

    def test_EQ_to_DDMMYYYY(self):
        value = "12/07/2023"
        actual = to_date(value, display_as="DDMMYYYY")
        expected = "12072023"
        self.assertEqual(expected, actual)

    def test_EQ_to_DDMMYY(self):
        value = "12/07/2023"
        actual = to_date(value, display_as="DDMMYY")
        expected = "120723"
        self.assertEqual(expected, actual)

    def test_EQ_to_YYYYMM(self):
        value = "12/07/2023"
        actual = to_date(value, display_as="YYYYMM")
        expected = "202307"
        self.assertEqual(expected, actual)

    def test_YYMMDD_to_DDMMYYYY(self):
        value = "230712"
        actual = to_date(value, input_format="YYMMDD", display_as="DDMMYYYY")
        expected = "12072023"
        self.assertEqual(expected, actual)

    def test_with_extra_chars(self):
        value = "12-07-23"
        actual = to_date(value, input_format="DD-MM-YY", display_as="YYYY_MM_DD")
        expected = "2023_07_12"
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

    def test_some_empty_dont_fail(self):
        value = "12/07/2023"
        values = [Empty, Empty]
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_all_empty_returns_empty(self):
        value = Empty
        values = [Empty, Empty, Empty]
        actual = any_date(value, values=values, on_true="1", on_false="2")
        expected = Empty
        self.assertEqual(expected, actual)


class StartOfMonthTests(unittest.TestCase):

    def test_MMYYYY(self):
        value = "072023"
        actual = start_of_month(value, input_format="MMYYYY", display_as="DDMMYYYY")
        expected = "01072023"
        self.assertEqual(expected, actual)

    def test_YYYYMM(self):
        value = "202307"
        actual = start_of_month(value, input_format="YYYYMM", display_as="DDMMYYYY")
        expected = "01072023"
        self.assertEqual(expected, actual)


class EndOfMonthTests(unittest.TestCase):

    def test_jul(self):
        value = "202307"
        actual = end_of_month(value, input_format="YYYYMM", display_as="DDMMYYYY")
        expected = "31072023"
        self.assertEqual(expected, actual)

    def test_sep(self):
        value = "202309"
        actual = end_of_month(value, input_format="YYYYMM", display_as="DDMMYYYY")
        expected = "30092023"
        self.assertEqual(expected, actual)

    def test_feb(self):
        value = "202302"
        actual = end_of_month(value, input_format="YYYYMM", display_as="DDMMYYYY")
        expected = "28022023"
        self.assertEqual(expected, actual)

    def test_feb_leap_year(self):
        value = "202402"
        actual = end_of_month(value, input_format="YYYYMM", display_as="DDMMYYYY")
        expected = "29022024"
        self.assertEqual(expected, actual)

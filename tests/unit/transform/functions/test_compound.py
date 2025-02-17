import unittest

from app.definitions.data import Empty
from app.services.transform.functions.compound import currency_thousands


class CurrencyTests(unittest.TestCase):

    def test_currency_thousands(self):
        tests = {
            "3": "0",
            "78": "0",
            "499": "0",
            "500": "1",
            "1306": "1",
            "1500": "2",
            "7805": "8",
            "357899": "358",
            "4999999": "5000"
        }
        for value, expected in tests.items():
            actual = currency_thousands(value)
            self.assertEqual(expected, actual, f"{value} should have rounded to {expected}")

    def test_currency_thousands_negatives(self):
        tests = {
            "-3": "0",
            "-78": "0",
            "-499": "0",
            "-500": "-1",
            "-1306": "-1",
            "-1500": "-2",
            "-7805": "-8",
            "-357899": "-358",
            "-4999999": "-5000"
        }
        for value, expected in tests.items():
            actual = currency_thousands(value)
            self.assertEqual(expected, actual, f"{value} should have rounded to {expected}")

    def test_empty_returns_empty(self):
        actual = currency_thousands(Empty)
        expected = Empty
        self.assertEqual(expected, actual)

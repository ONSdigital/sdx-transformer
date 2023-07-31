import unittest

from app.formatters.formatter import Formatter


class ConvertPeriodTests(unittest.TestCase):

    def test_DDMMYY_to_DDMMYY(self):
        period = "310723"
        actual = Formatter("DDMMYY", "DDMMYY").convert_period(period)
        expected = "310723"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_MMYY(self):
        period = "310723"
        actual = Formatter("DDMMYY", "MMYY").convert_period(period)
        expected = "0723"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_YYMMDD(self):
        period = "310723"
        actual = Formatter("DDMMYY", "YYMMDD").convert_period(period)
        expected = "230731"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_YYYY(self):
        period = "310723"
        actual = Formatter("DDMMYY", "YYYY").convert_period(period)
        expected = "2023"
        self.assertEqual(expected, actual)

    def test_MMYYYY_to_YYYY(self):
        period = "072023"
        actual = Formatter("MMYYYY", "YYYY").convert_period(period)
        expected = "2023"
        self.assertEqual(expected, actual)

    def test_YYYYMM_to_YYYYMM(self):
        period = "202307"
        actual = Formatter("YYYYMM", "YYYYMM").convert_period(period)
        expected = "202307"
        self.assertEqual(expected, actual)

    def test_YYYY_to_YY(self):
        period = "2023"
        actual = Formatter("YYYY", "YY").convert_period(period)
        expected = "23"
        self.assertEqual(expected, actual)

    def test_YYYYMMDD_to_MMYYYY(self):
        period = "20230731"
        actual = Formatter("YYYYMMDD", "MMYYYY").convert_period(period)
        expected = "072023"
        self.assertEqual(expected, actual)

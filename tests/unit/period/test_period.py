import unittest

from app.services.period.period import Period, PeriodFormatError


class ConvertPeriodTests(unittest.TestCase):

    def test_DDMMYY_to_DDMMYY(self):
        period = Period("310723", "DDMMYY")
        actual = period.convert_to_format("DDMMYY")
        expected = "310723"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_MMYY(self):
        period = Period("310723", "DDMMYY")
        actual = period.convert_to_format("MMYY")
        expected = "0723"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_YYMMDD(self):
        period = Period("310723", "DDMMYY")
        actual = period.convert_to_format("YYMMDD")
        expected = "230731"
        self.assertEqual(expected, actual)

    def test_DDMMYY_to_YYYY(self):
        period = Period("310723", "DDMMYY")
        actual = period.convert_to_format("YYYY")
        expected = "2023"
        self.assertEqual(expected, actual)

    def test_MMYYYY_to_YYYY(self):
        period = Period("072023", "MMYYYY")
        actual = period.convert_to_format("YYYY")
        expected = "2023"
        self.assertEqual(expected, actual)

    def test_YYYYMM_to_YYYYMM(self):
        period = Period("202307", "YYYYMM")
        actual = period.convert_to_format("YYYYMM")
        expected = "202307"
        self.assertEqual(expected, actual)

    def test_YYYY_to_YY(self):
        period = Period("2023", "YYYY")
        actual = period.convert_to_format("YY")
        expected = "23"
        self.assertEqual(expected, actual)

    def test_YYYYMMDD_to_MMYYYY(self):
        period = Period("20230731", "YYYYMMDD")
        actual = period.convert_to_format("MMYYYY")
        expected = "072023"
        self.assertEqual(expected, actual)

    def test_incorrect_format_uses_default_value(self):
        period = Period("202310", "YY")
        actual = period.convert_to_format("YY")
        expected = "23"
        self.assertEqual(expected, actual)

    def test_incorrect_format_uses_default_value_length_4(self):
        period = Period("2301", "YY")
        actual = period.convert_to_format("YY")
        expected = "23"
        self.assertEqual(expected, actual)

    def test_incorrect_format_uses_default_value_length_4_with_different_pck_format(self):
        period = Period("2301", "YYYYMM")
        actual = period.convert_to_format("YYYYMM")
        expected = "202301"
        self.assertEqual(expected, actual)

    def test_incorrect_format_uses_default_value_length_2(self):
        period = Period("23", "YYYYMM")
        actual = period.convert_to_format("YYYYMM")
        expected = "202301"
        self.assertEqual(expected, actual)


class ComparePeriodTests(unittest.TestCase):

    def test_gt_YYYYMM(self):
        period1 = Period("202503", "YYYYMM")
        period2 = Period("202502", "YYYYMM")
        self.assertTrue(period1 > period2)

    def test_gt_DDMMYY(self):
        period1 = Period("010124", "DDMMYY")
        period2 = Period("311223", "DDMMYY")
        self.assertTrue(period1 > period2)

    def test_gt_YYMM(self):
        period1 = Period("2401", "YYMM")
        period2 = Period("2312", "YYMM")
        self.assertTrue(period1 > period2)

    def test_gt_MMYYYY(self):
        period1 = Period("012024", "MMYYYY")
        period2 = Period("122023", "MMYYYY")
        self.assertTrue(period1 > period2)

    def test_gt_YYYYMMDD(self):
        period1 = Period("20240101", "YYYYMMDD")
        period2 = Period("20231231", "YYYYMMDD")
        self.assertTrue(period1 > period2)

    def test_gt_YYYYMM_YYMM(self):
        period1 = Period("202503", "YYYYMM")
        period2 = Period("2502", "YYMM")
        self.assertTrue(period1 > period2)

    def test_gt_YYYY_YY(self):
        period1 = Period("2025", "YYYY")
        period2 = Period("24", "YY")
        self.assertTrue(period1 > period2)

    def test_gt_incompatible(self):
        period1 = Period("2025", "YYYY")
        period2 = Period("2504", "YYMM")
        with self.assertRaises(PeriodFormatError):
            _ = period1 > period2

    def test_ge_YYYYMM(self):
        period1 = Period("202503", "YYYYMM")
        period2 = Period("202502", "YYYYMM")
        period3 = Period("202503", "YYYYMM")
        self.assertTrue(period1 >= period2)
        self.assertTrue(period1 >= period3)

    def test_ge_DDMMYY(self):
        period1 = Period("010124", "DDMMYY")
        period2 = Period("311223", "DDMMYY")
        period3 = Period("010124", "DDMMYY")
        self.assertTrue(period1 >= period2)
        self.assertTrue(period1 >= period3)

    def test_ge_YYMM(self):
        period1 = Period("2401", "YYMM")
        period2 = Period("2312", "YYMM")
        period3 = Period("2401", "YYMM")
        self.assertTrue(period1 >= period2)
        self.assertTrue(period1 >= period3)

    def test_ge_MMYYYY(self):
        period1 = Period("012024", "MMYYYY")
        period2 = Period("122023", "MMYYYY")
        period3 = Period("012024", "MMYYYY")
        self.assertTrue(period1 >= period2)
        self.assertTrue(period1 >= period3)

    def test_ge_YYYYMMDD(self):
        period1 = Period("20240101", "YYYYMMDD")
        period2 = Period("20231231", "YYYYMMDD")
        period3 = Period("20240101", "YYYYMMDD")
        self.assertTrue(period1 >= period2)
        self.assertTrue(period1 >= period3)

    def test_le_YYYYMM(self):
        period1 = Period("202502", "YYYYMM")
        period2 = Period("202503", "YYYYMM")
        period3 = Period("202502", "YYYYMM")
        self.assertTrue(period1 <= period2)
        self.assertTrue(period1 <= period3)

    def test_le_DDMMYY(self):
        period1 = Period("311223", "DDMMYY")
        period2 = Period("010124", "DDMMYY")
        period3 = Period("311223", "DDMMYY")
        self.assertTrue(period1 <= period2)
        self.assertTrue(period1 <= period3)

    def test_le_YYMM(self):
        period1 = Period("2312", "YYMM")
        period2 = Period("2401", "YYMM")
        period3 = Period("2312", "YYMM")
        self.assertTrue(period1 <= period2)
        self.assertTrue(period1 <= period3)

    def test_le_MMYYYY(self):
        period1 = Period("122023", "MMYYYY")
        period2 = Period("012024", "MMYYYY")
        period3 = Period("122023", "MMYYYY")
        self.assertTrue(period1 <= period2)
        self.assertTrue(period1 <= period3)

    def test_le_YYYYMMDD(self):
        period1 = Period("20231231", "YYYYMMDD")
        period2 = Period("20240101", "YYYYMMDD")
        period3 = Period("20231231", "YYYYMMDD")
        self.assertTrue(period1 <= period2)
        self.assertTrue(period1 <= period3)

    def test_lt_YYYYMM(self):
        period1 = Period("202502", "YYYYMM")
        period2 = Period("202503", "YYYYMM")
        self.assertTrue(period1 < period2)

    def test_lt_DDMMYY(self):
        period1 = Period("311223", "DDMMYY")
        period2 = Period("010124", "DDMMYY")
        self.assertTrue(period1 < period2)

    def test_lt_YYMM(self):
        period1 = Period("2312", "YYMM")
        period2 = Period("2401", "YYMM")
        self.assertTrue(period1 < period2)

    def test_lt_MMYYYY(self):
        period1 = Period("122023", "MMYYYY")
        period2 = Period("012024", "MMYYYY")
        self.assertTrue(period1 < period2)

    def test_lt_YYYYMMDD(self):
        period1 = Period("20231231", "YYYYMMDD")
        period2 = Period("20240101", "YYYYMMDD")
        self.assertTrue(period1 < period2)

import unittest

from app.definitions import Empty
from app.functions.standard import contains, any_contains, any_date, exists, concat, any_exists, starts_with


class StartsWithTests(unittest.TestCase):

    def test_empty(self):
        value = Empty
        actual = starts_with(value, match_str="sent", on_true="1", on_false="2")
        expected = Empty
        self.assertEqual(expected, actual)

    def test_true(self):
        value = "sentence for testing purposes"
        actual = starts_with(value, match_str="sent", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = "sentence for testing purposes"
        actual = starts_with(value, match_str=" sent", on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)


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

    def test_empty_returns_empty(self):
        value = Empty
        actual = contains(value, match_str="I don't exist", on_true="1", on_false="2")
        expected = Empty
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

    def test_empty_doesnt_fail(self):
        value = Empty
        values = ["yes", "no", Empty]
        actual = any_contains(value, values=values, match_str="y", on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_all_empty_returns_empty(self):
        value = Empty
        values = [Empty, Empty, Empty]
        actual = any_contains(value, values=values, match_str="y", on_true="1", on_false="2")
        expected = Empty
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


class AnyExistTests(unittest.TestCase):

    def test_true(self):
        value = "foo"
        values = [Empty, Empty]
        actual = any_exists(value, values=values, on_true="1", on_false="2")
        expected = "1"
        self.assertEqual(expected, actual)

    def test_false(self):
        value = Empty
        values = [Empty, Empty]
        actual = any_exists(value, values=values, on_true="1", on_false="2")
        expected = "2"
        self.assertEqual(expected, actual)


class ConcatTests(unittest.TestCase):

    def test_all_empty_returns_empty(self):
        value = Empty
        values = [Empty, Empty]
        actual = concat(value, values=values)
        expected = Empty
        self.assertEqual(expected, actual)

    def test_simple(self):
        value = "a"
        values = ["b", "c"]
        actual = concat(value, values=values, seperator="-")
        expected = "a-b-c"
        self.assertEqual(expected, actual)

    def test_no_fail_on_empty(self):
        value = "a"
        values = [Empty, "c"]
        actual = concat(value, values=values, seperator="_")
        expected = "a_c"
        self.assertEqual(expected, actual)
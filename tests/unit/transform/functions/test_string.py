import unittest

from app.definitions import Empty
from app.transform.functions.string import contains, any_contains, concat, starts_with, carve


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


class CarveTest(unittest.TestCase):

    def test_all_empty_returns_empty(self):
        value = Empty
        actual = carve(value)
        expected = Empty
        self.assertEqual(expected, actual)

    def test_simple(self):
        value = "112185561111"
        actual = carve(value, end_index=3)
        expected = "112"
        self.assertEqual(expected, actual)

    def test_with_no_index(self):
        value = "123456789"
        actual = carve(value)
        expected = "1234"
        self.assertEqual(expected, actual)

    def test_with_start_and_end(self):
        value = "123456789"
        actual = carve(value, start_index=2, end_index=5)
        expected = "345"
        self.assertEqual(expected, actual)

    def test_with_vat_ref(self):
        value = "112185561111"
        first = carve(value, end_index=9)
        second = carve(value, start_index=9)

        self.assertEqual(["112185561", "111"], [first, second])


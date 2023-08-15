import unittest

from app.pck import get_build_spec, transform
from tests.integration.pck import remove_empties


class BricksPckTests(unittest.TestCase):

    def test_bricks_prepend(self):
        submission_data = {"01": "10", "9999": "Concrete"}

        build_spec = get_build_spec("074")
        transformed_data = transform(submission_data, build_spec)
        actual = remove_empties(transformed_data)

        expected = {"301": "10"}
        self.assertEqual(expected, actual)


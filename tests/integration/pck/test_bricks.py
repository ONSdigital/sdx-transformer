import unittest

from app.pck import get_build_spec, transform
from tests.integration.pck import remove_empties


class BricksPckTests(unittest.TestCase):

    def test_bricks_prepend(self):
        types = {
            "Clay": "2",
            "Concrete": "3",
            "Sandlime": "4"
        }
        submission_data = {"01": "10",
                           "02": "11",
                           "03": "12",
                           "04": "13",
                           "11": "14",
                           "12": "15",
                           "13": "16",
                           "14": "17",
                           "21": "18",
                           "22": "19",
                           "23": "20",
                           "24": "21",
                           "9999": "Concrete"}

        build_spec = get_build_spec("074")

        for k, v in types.items():
            submission_data["9999"] = k
            expected = {f"{v}01": "10",
                        f"{v}02": "11",
                        f"{v}03": "12",
                        f"{v}04": "13",
                        f"{v}11": "14",
                        f"{v}12": "15",
                        f"{v}13": "16",
                        f"{v}14": "17",
                        f"{v}21": "18",
                        f"{v}22": "19",
                        f"{v}23": "20",
                        f"{v}24": "21"}
            transformed_data = transform(submission_data, build_spec)
            actual = remove_empties(transformed_data)
            self.assertEqual(expected, actual)

    def test_bricks_text_transform(self):
        submission_data = {"145": "I am a comment that should be replaced with a 1",
                           "146": ""}

        build_spec = get_build_spec("074")

        expected = {"145": "1",
                    "146": "2"}
        transformed_data = transform(submission_data, build_spec)
        actual = remove_empties(transformed_data)
        self.assertEqual(expected, actual)


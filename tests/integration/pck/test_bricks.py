import unittest

from app.definitions import SurveyMetadata
from app.pck import get_build_spec, transform
from tests.integration.pck import remove_empties, read_submission_data


class BricksTransformsTests(unittest.TestCase):

    def test_bricks_prepend(self):
        types = {
            "Clay": "2",
            "Concrete": "3",
            "Sandlime": "4"
        }
        submission_data = {"01": "0",
                           "02": "0",
                           "03": "0",
                           "04": "0",
                           "11": "0",
                           "12": "0",
                           "13": "0",
                           "14": "0",
                           "21": "0",
                           "22": "0",
                           "23": "0",
                           "24": "0",
                           "9999": "Concrete"}

        build_spec = get_build_spec("074")

        for k, v in types.items():
            submission_data["9999"] = k
            expected = {f"{v}01": "0",
                        f"{v}02": "0",
                        f"{v}03": "0",
                        f"{v}04": "0",
                        f"{v}11": "0",
                        f"{v}12": "0",
                        f"{v}13": "0",
                        f"{v}14": "0",
                        f"{v}21": "0",
                        f"{v}22": "0",
                        f"{v}23": "0",
                        f"{v}24": "0",
                        "145": "2",
                        "146": "2",
                        "501": "0",
                        "502": "0",
                        "503": "0",
                        "504": "0"}
            transformed_data = transform(submission_data, build_spec)
            actual = remove_empties(transformed_data)
            actual = actual.keys()
            expected = expected.keys()
            self.assertEqual(expected, actual)

    def test_bricks_text_transform(self):
        submission_data = {"145": "I am a comment that should be replaced with a 1",
                           "146": ""}

        build_spec = get_build_spec("074")

        expected = {"145": "1",
                    "146": "2",
                    "501": "0",
                    "502": "0",
                    "503": "0",
                    "504": "0"}
        transformed_data = transform(submission_data, build_spec)
        actual = remove_empties(transformed_data)
        self.assertEqual(expected, actual)

    def test_bricks_totals_transform(self):
        types = {
            "Clay": "2",
            "Concrete": "3",
            "Sandlime": "4"
        }
        submission_data = {"01": "10",
                           "11": "1",
                           "21": "1",
                           "02": "100",
                           "12": "10",
                           "22": "10",
                           "03": "50",
                           "13": "100",
                           "23": "100",
                           "04": "1",
                           "14": "6",
                           "24": "7",
                           "9999": ""}

        build_spec = get_build_spec("074")

        for k, v in types.items():
            submission_data["9999"] = k
            expected = {f"{v}01": "10",
                        f"{v}11": "1",
                        f"{v}21": "1",
                        f"{v}02": "100",
                        f"{v}12": "10",
                        f"{v}22": "10",
                        f"{v}03": "50",
                        f"{v}13": "100",
                        f"{v}23": "100",
                        f"{v}04": "1",
                        f"{v}14": "6",
                        f"{v}24": "7",
                        "145": "2",
                        "146": "2",
                        "501": "12",
                        "502": "120",
                        "503": "250",
                        "504": "14"
                        }
            transformed_data = transform(submission_data, build_spec)
            actual = remove_empties(transformed_data)
            self.assertEqual(expected, actual)


class BricksPckTests(unittest.TestCase):
    filepath = "tests/data/bricks/074.0001.json"
    submission_data = read_submission_data(filepath)

    survey_metadata: SurveyMetadata = {
            "survey_id": "074",
            "period_id": "201605",
            "ref_period_start_date": "2016-05-01",
            "ref_period_end_date": "2016-05-31"
        }

    # TODO finish test

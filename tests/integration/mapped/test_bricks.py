import unittest

from app.repositories.file_repository import BuildSpecFileRepository
from app.definitions.spec import ParseTree
from app.definitions.data import SurveyMetadata, PCK
from app.pck_managers.flat import transform, get_pck
from app.transform.interpolate import interpolate
from app.transform.populate import resolve_value_fields
from tests.integration.mapped import remove_empties, read_submission_data, are_equal


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

            build_spec = BuildSpecFileRepository().get_build_spec("bricks")
            parse_tree: ParseTree = resolve_value_fields(interpolate(build_spec["template"], build_spec["transforms"]))
            transformed_data = transform(submission_data, parse_tree)
            actual = remove_empties(transformed_data)
            actual = actual.keys()
            expected = expected.keys()
            self.assertEqual(expected, actual)

    def test_bricks_text_transform(self):
        submission_data = {"145": "I am a comment that should be replaced with a 1",
                           "146": ""}

        expected = {"145": "1",
                    "146": "2",
                    "501": "0",
                    "502": "0",
                    "503": "0",
                    "504": "0"}

        build_spec = BuildSpecFileRepository().get_build_spec("bricks")
        parse_tree: ParseTree = resolve_value_fields(interpolate(build_spec["template"], build_spec["transforms"]))
        transformed_data = transform(submission_data, parse_tree)
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

            build_spec = BuildSpecFileRepository().get_build_spec("bricks")
            parse_tree: ParseTree = resolve_value_fields(interpolate(build_spec["template"], build_spec["transforms"]))
            transformed_data = transform(submission_data, parse_tree)
            actual = remove_empties(transformed_data)
            self.assertEqual(expected, actual)


class BricksPckTests(unittest.TestCase):

    def test_0002_to_pck(self):
        filepath = "tests/data/bricks/074.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "074",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/bricks/074.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

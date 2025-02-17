import unittest

from app.config.dependencies import get_flat_transformer, get_build_spec_mapping, get_spec_repository, get_executor, \
    get_formatter_mapping, get_func_lookup
from app.controllers.flat import get_pck
from app.definitions.data import SurveyMetadata, PCK
from app.definitions.spec import ParseTree
from tests.integration.mapped import remove_empties, read_submission_data, are_equal

survey_metadata: SurveyMetadata = {
    "survey_id": "074",
    "period_id": "201605",
    "ru_ref": "12346789012A",
    "form_type": "0001",
    "period_start_date": "2016-05-01",
    "period_end_date": "2016-05-31",
}


class BricksTransformsTests(unittest.TestCase):

    def setUp(self):
        self.transformer = get_flat_transformer(
            survey_metadata,
            get_build_spec_mapping(get_spec_repository()),
            get_executor(get_func_lookup()),
            get_formatter_mapping(),
        )

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

            transformer = self.transformer
            parse_tree: ParseTree = transformer.interpolate()
            transformed_data = transformer.run(parse_tree, submission_data)
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

        transformer = self.transformer
        parse_tree: ParseTree = transformer.interpolate()
        transformed_data = transformer.run(parse_tree, submission_data)
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

            transformer = self.transformer
            parse_tree: ParseTree = transformer.interpolate()
            transformed_data = transformer.run(parse_tree, submission_data)
            actual = remove_empties(transformed_data)
            self.assertEqual(expected, actual)


class BricksPckTests(unittest.TestCase):

    def test_0002_to_pck(self):
        filepath = "tests/data/bricks/074.0001.json"
        submission_data = read_submission_data(filepath)
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/bricks/074.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

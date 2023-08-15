import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_pck
from tests.integration.pck import read_submission_data, are_equal


class UKISPckTests(unittest.TestCase):

    def test_0001_to_pck(self):
        self.maxDiff = None
        filepath = "tests/data/mes/092.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_minimal_to_pck(self):
        self.maxDiff = None
        filepath = "tests/data/mes/092.0001.min.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "58153646441",
            "form_type": "0001",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.min.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_round_up_to_pck(self):
        self.maxDiff = None
        filepath = "tests/data/mes/092.0001.round_up.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.round_up.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

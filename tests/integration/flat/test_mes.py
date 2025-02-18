import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import get_pck
from tests.integration.flat import read_submission_data, are_equal


class UKISPckTests(unittest.TestCase):

    def test_0001_to_pck(self):
        filepath = "tests/data/mes/092.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_minimal_to_pck(self):
        filepath = "tests/data/mes/092.0001.min.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "58153646441",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.min.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_round_up_to_pck(self):
        filepath = "tests/data/mes/092.0001.round_up.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "092",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mes/092.0001.round_up.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

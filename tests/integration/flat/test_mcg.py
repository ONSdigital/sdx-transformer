import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import flat_to_pck
from tests.integration.flat import read_submission_data, are_equal


class MCGPckTests(unittest.TestCase):

    def test_0001_to_pck(self):
        filepath = "tests/data/mcg/127.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "127",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = flat_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mcg/127.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0002_to_pck(self):
        filepath = "tests/data/mcg/127.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "127",
            "period_id": "202307",
            "ru_ref": "12346789012A",
            "form_type": "0002",
            "period_start_date": "2023-07-01",
            "period_end_date": "20223-07-31",
        }

        actual: PCK = flat_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mcg/127.0002.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_fail_to_pck(self):
        filepath = "tests/data/mcg/fail.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "127",
            "period_id": "202307",
            "ru_ref": "11110000020H",
            "form_type": "0001",
            "period_start_date": "2023-07-01",
            "period_end_date": "20223-07-31",
        }

        actual: PCK = flat_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mcg/fail.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

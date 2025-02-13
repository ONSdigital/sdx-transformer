import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class QBSTest(unittest.TestCase):

    def test_0001_to_pck(self):
        filepath = "tests/data/qbs/139.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "139",
            "period_id": "1604",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_start_date": "2016-04-01",
            "period_end_date": "2016-10-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qbs/139.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_missing_total_to_pck(self):
        filepath = "tests/data/qbs/139.0001.missing.total.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "139",
            "period_id": "1604",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_start_date": "2016-04-01",
            "period_end_date": "2016-10-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qbs/139.0001.missing.total.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_zero_total_to_pck(self):
        filepath = "tests/data/qbs/139.0001.zero.total.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "139",
            "period_id": "1604",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_start_date": "2016-04-01",
            "period_end_date": "2016-10-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qbs/139.0001.zero.total.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

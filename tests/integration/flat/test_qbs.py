import json
import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import get_pck
from tests.integration.flat import read_submission_data, are_equal


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

    def test_0001_to_spp(self):
        filepath = "tests/data/qbs/139.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "139",
            "period_id": "2507",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_start_date": "2025-03-01",
            "period_end_date": "2025-06-01",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qbs/139.0001-spp.json"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(json.loads(expected), json.loads(actual))

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

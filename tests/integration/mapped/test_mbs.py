import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class MBSPckTests(unittest.TestCase):

    def test_0106_to_pck(self):
        filepath = "tests/data/mbs/009.0106.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "009",
            "period_id": "1605",
            "ru_ref": "30237487572l",
            "form_type": "0106",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        print(actual)

        pck_filepath = "tests/data/mbs/009.0106.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0111_to_pck(self):
        filepath = "tests/data/mbs/009.0111.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "009",
            "period_id": "1605",
            "ru_ref": "46588678052M",
            "form_type": "0111",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mbs/009.0111.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0255_to_pck(self):
        filepath = "tests/data/mbs/009.0255.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "009",
            "period_id": "1605",
            "ru_ref": "97148856319Y",
            "form_type": "0255",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mbs/009.0255.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0867_to_pck(self):
        filepath = "tests/data/mbs/009.0867.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "009",
            "period_id": "1605",
            "ru_ref": "97148856319Y",
            "form_type": "0255",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        print(actual)

        pck_filepath = "tests/data/mbs/009.0867.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

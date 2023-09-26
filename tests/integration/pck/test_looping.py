import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_pck
from tests.integration.pck import read_submission_data, are_equal


class UKISPckTests(unittest.TestCase):

    def test_0001_to_spp(self):
        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "001",
            "period_id": "202212",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/looping/looping-example-spp.json"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))
import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.controllers.flat import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class QPSESRAPPckTests(unittest.TestCase):

    def test_0003_to_pck(self):
        filepath = "tests/data/qpsesrap/169.0003.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "169",
            "period_id": "1605",
            "ru_ref": "12346789012A",
            "form_type": "0003",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qpsesrap/169.0003.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import flat_to_pck
from tests.integration.flat import read_submission_data, are_equal


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

        actual: PCK = flat_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qpsesrap/169.0003.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

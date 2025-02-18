import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import get_pck
from tests.integration.flat import read_submission_data, are_equal


class QPSESPckTests(unittest.TestCase):

    def test_0002_to_pck(self):
        filepath = "tests/data/qpses/160.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "160",
            "period_id": "1605",
            "ru_ref": "12346789012A",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/qpses/160.0002.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

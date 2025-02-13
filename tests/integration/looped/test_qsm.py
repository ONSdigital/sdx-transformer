import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.pck_managers.looped import get_looping
from tests.integration.looped import read_submission_data
from tests.integration.mapped import are_equal


class QsmTests(unittest.TestCase):

    def test_to_cs_pck(self):

        filepath = "tests/data/marine/076.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "076",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/marine/076.0002.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

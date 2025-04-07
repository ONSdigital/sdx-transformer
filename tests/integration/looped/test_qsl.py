import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.controllers.looped import looping_to_pck
from tests.integration.looped import read_submission_data
from tests.integration.flat import are_equal


class QslTests(unittest.TestCase):

    def test_to_cs_pck(self):

        filepath = "tests/data/land/066.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "066",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = looping_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/land/066.0002.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

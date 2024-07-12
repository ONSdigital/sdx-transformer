import json
import unittest

from app.definitions import SurveyMetadata, ImageResponse, PCK
from app.pck_managers.looped import get_looping
from tests.integration.looped import read_submission_data
from tests.integration.mapped import are_equal


class BresTests(unittest.TestCase):

    def test_to_idbr_pck(self):

        filepath = "tests/data/bres/looping_bres_input_no_lu_data.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0019",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        print("")
        print(actual)

        pck_filepath = "tests/data/bres/looping_bres_no_lu.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        # self.assertTrue(are_equal(expected, actual))

import os
import unittest

from app.definitions.input import Data, SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import flat_to_pck
from tests.integration.flat import read_submission_data, are_equal


class ABSPckTests(unittest.TestCase):

    def test_abs_to_pck(self):
        root_dir = "tests/data/abs/"
        json_file_names = [f for f in os.listdir(root_dir) if f.endswith(".json")]
        print("------------")
        for filename in json_file_names:

            print("testing " + filename)
            filepath = root_dir + filename
            form_type = filename.split(".")[1]
            submission_data: Data = read_submission_data(filepath)

            survey_metadata: SurveyMetadata = {
                "survey_id": "202",
                "period_id": "21",
                "ru_ref": "12346789012A",
                "form_type": form_type,
                "period_start_date": "2021-01-01",
                "period_end_date": "2021-12-31",
            }

            actual: PCK = flat_to_pck(submission_data, survey_metadata)

            pck_filepath = root_dir + filename.replace("json", "pck")
            with open(pck_filepath) as f:
                expected: PCK = f.read()

            passed = are_equal(expected, actual)
            if not passed:
                print(f"\n Failed test for {filename}")
                print(actual)

            self.assertTrue(passed)

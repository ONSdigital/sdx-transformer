import os
import unittest

from app.definitions.input import Data, SurveyMetadata
from app.definitions.output import PCK
from app.controllers.flat import flat_to_pck
from tests.integration.flat import read_submission_data, are_equal


class StocksPckTests(unittest.TestCase):

    def test_stocks_to_pck(self):
        root_dir = "tests/data/stocks/"
        json_file_names = [f for f in os.listdir(root_dir) if f.endswith(".json")]
        print("-----------------")
        for filename in json_file_names:

            print("testing " + filename)
            filepath = root_dir + filename
            form_type = filename.split(".")[1]
            submission_data: Data = read_submission_data(filepath)

            survey_metadata: SurveyMetadata = {
                "survey_id": "017",
                "period_id": "1904",
                "ru_ref": "15162882666F",
                "form_type": form_type,
                "period_start_date": "2019-01-01",
                "period_end_date": "2019-04-30",
            }

            actual: PCK = flat_to_pck(submission_data, survey_metadata)

            pck_filepath = root_dir + filename.replace("json", "pck")
            with open(pck_filepath) as f:
                expected: PCK = f.read()

            self.assertTrue(are_equal(expected, actual))

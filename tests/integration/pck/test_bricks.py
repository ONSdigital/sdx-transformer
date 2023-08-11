import os
import unittest

from app.definitions import Data, SurveyMetadata, PCK
from app.pck import get_pck
from tests.integration.pck import read_submission_data, convert_pck_to_dict


class BricksPckTests(unittest.TestCase):

    def test_bricks_to_pck(self):
        root_dir = "tests/data/bricks/"
        json_file_names = [f for f in os.listdir(root_dir) if f.endswith(".json")]
        print("------------")
        for filename in json_file_names:

            print("testing " + filename)
            filepath = root_dir + filename
            form_type = filename.split(".")[1]
            submission_data: Data = read_submission_data(filepath)

            survey_metadata: SurveyMetadata = {
                "survey_id": "202",
                "period_id": "202112",
                "ru_ref": "12346789012A",
                "form_type": form_type,
            }

            pck: PCK = get_pck(submission_data, survey_metadata)
            actual = convert_pck_to_dict(pck)

            pck_filepath = root_dir + filename.replace("json", "pck")
            with open(pck_filepath) as f:
                text: PCK = f.read()

            expected = convert_pck_to_dict(text)

            self.assertEqual(expected, actual)


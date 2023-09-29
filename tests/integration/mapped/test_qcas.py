import os
import unittest

from app.definitions import SurveyMetadata, PCK, Data
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class QCASPckTests(unittest.TestCase):

    def test_qcas_to_pck(self):
        root_dir = "tests/data/qcas/"
        json_file_names = [f for f in os.listdir(root_dir) if f.endswith(".json")]
        print("-----------------")
        for filename in json_file_names:

            print("testing " + filename)
            filepath = root_dir + filename
            form_type = filename.split(".")[1]
            submission_data: Data = read_submission_data(filepath)

            survey_metadata: SurveyMetadata = {
                "survey_id": "019",
                "period_id": "2301",
                "ru_ref": "12346789012A",
                "form_type": form_type,
                "period_start_date": "2023-01-01",
                "period_end_date": "2023-03-31",
            }

            actual: PCK = get_pck(submission_data, survey_metadata)

            pck_filepath = root_dir + filename.replace("json", "pck")
            with open(pck_filepath) as f:
                expected: PCK = f.read()

            self.assertTrue(are_equal(expected, actual))

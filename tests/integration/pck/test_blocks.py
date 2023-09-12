import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_build_spec, transform, get_pck
from tests.integration.pck import remove_empties, read_submission_data, are_equal


class BlocksPckTests(unittest.TestCase):
    def test_0002_to_pck(self):
        filepath = "tests/data/blocks/073.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "073",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "20216-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/blocks/073.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

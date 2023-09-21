import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_build_spec, transform, get_pck
from tests.integration.pck import remove_empties, read_submission_data, are_equal


class ConstructionPckTests(unittest.TestCase):
    def test_0001_to_pck(self):
        filepath = "tests/data/construction/228.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "48514665167x",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

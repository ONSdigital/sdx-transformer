import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_pck
from tests.integration.pck import read_submission_data, are_equal


class StocksPckTests(unittest.TestCase):

    def test_0001_to_pck(self):
        filepath = "tests/data/stocks/017.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "017",
            "period_id": "1904",
            "ru_ref": "15162882666F",
            "form_type": "0001",
            "period_start_date": "2019-01-01",
            "period_end_date": "2019-04-30",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        print(actual)

        pck_filepath = "tests/data/stocks/017.0001.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))
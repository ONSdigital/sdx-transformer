import json
import unittest

from app.definitions.input import SurveyMetadata
from app.controllers.flat import flat_to_pck
from tests.integration.flat import read_submission_data


class RailsTests(unittest.TestCase):

    def test_0001_to_json(self):
        filepath = "tests/data/rails/194.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "194",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        result: str = flat_to_pck(submission_data, survey_metadata)
        actual: dict[str, str] = json.loads(result)

        pck_filepath = "tests/data/rails/result.json"
        with open(pck_filepath) as f:
            expected: dict[str, str] = json.load(f)

        self.assertEqual(expected, actual)

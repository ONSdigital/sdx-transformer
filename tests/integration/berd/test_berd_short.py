import json
import unittest

from app.definitions import SurveyMetadata, ImageResponse, SPP
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data


class BerdTests(unittest.TestCase):

    def test_to_pck(self):

        filepath = "tests/data/berd/002.0006.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "tx_id": "ea82c224-0f80-41cc-b877-8a7804b56c26",
            "survey_id": "002",
            "period_id": "23",
            "ru_ref": "12346789012A",
            "form_type": "0006",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: SPP = json.loads(get_pck(submission_data, survey_metadata))

        spp_filepath = "tests/data/berd/002.0006-spp.json"
        with open(spp_filepath) as f:
            expected: list[ImageResponse] = json.load(f)

        self.assertEqual(expected, actual)

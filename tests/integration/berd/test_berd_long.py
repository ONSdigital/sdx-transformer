import json
import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import SPP
from app.controllers.looped import get_looping
from tests.integration.looped import read_submission_data


class BerdTests(unittest.TestCase):

    def test_to_spp(self):

        filepath = "tests/data/berd/002.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "002",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: SPP = json.loads(get_looping(submission_data, survey_metadata))

        spp_filepath = "tests/data/berd/002.0001-spp.json"
        with open(spp_filepath) as f:
            expected: SPP = json.load(f)

        self.assertEqual(expected, actual)

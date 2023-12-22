import json
import unittest

from app.definitions import SurveyMetadata, ImageResponse, SPP
from app.pck_managers.looped import get_looping
from tests.integration.looped import read_submission_data


class BerdTests(unittest.TestCase):

    def test_to_image(self):
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

        actual: list[ImageResponse] = json.loads(get_looping(submission_data, survey_metadata, True))

        image_filepath = "tests/data/berd/002.0001-image.json"
        with open(image_filepath) as f:
            expected: list[ImageResponse] = json.load(f)

        expected.sort(key=lambda i: i['instance'])
        actual.sort(key=lambda i: i['instance'])

        # print(json.dumps(actual))

        self.assertEqual(expected, actual)

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

        actual: SPP = json.loads(get_looping(submission_data, survey_metadata, False))

        spp_filepath = "tests/data/berd/002.0001-spp.json"
        with open(spp_filepath) as f:
            expected: list[ImageResponse] = json.load(f)

        self.assertEqual(expected, actual)

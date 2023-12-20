import json
import unittest

from app.definitions import SurveyMetadata, ImageResponse
from app.pck_managers.looped import get_looping
from tests.integration.looped import read_submission_data


class QrtTests(unittest.TestCase):

    def test_to_image(self):

        filepath = "tests/data/tiles/068.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "068",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: list[ImageResponse] = json.loads(get_looping(submission_data, survey_metadata))

        spp_filepath = "tests/data/tiles/068-image.json"
        with open(spp_filepath) as f:
            expected: list[ImageResponse] = json.load(f)

        expected.sort(key=lambda i: i['instance'])
        actual.sort(key=lambda i: i['instance'])

        print(json.dumps(actual))

        self.assertEqual(expected, actual)

import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck import get_pck
from tests.integration.pck import read_submission_data, convert_pck_to_dict


class MCGPckTests(unittest.TestCase):

    def test_0001_to_pck(self):
        filepath = "tests/data/mcg/127.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "127",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
        }

        pck: PCK = get_pck(submission_data, survey_metadata)
        actual = convert_pck_to_dict(pck)

        print("")
        print(pck)

        pck_filepath = "tests/data/mcg/127.0001.pck"
        with open(pck_filepath) as f:
            text: PCK = f.read()

        expected = convert_pck_to_dict(text)
        self.assertEqual(expected, actual)

    def test_0002_to_pck(self):
        filepath = "tests/data/mcg/127.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "127",
            "period_id": "202307",
            "ru_ref": "12346789012A",
            "form_type": "0002",
        }

        pck: PCK = get_pck(submission_data, survey_metadata)
        actual = convert_pck_to_dict(pck)

        pck_filepath = "tests/data/mcg/127.0002.pck"
        with open(pck_filepath) as f:
            text: PCK = f.read()

        expected = convert_pck_to_dict(text)
        self.assertEqual(expected, actual)

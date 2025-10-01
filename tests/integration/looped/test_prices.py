import unittest

from app.controllers.looped import looping_to_pck
from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from tests.helpers import get_src_path
from tests.integration.looped import read_submission_data


class TestPrices(unittest.TestCase):
    def setUp(self):
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "132",
            "period_id": "201605",
            "ru_ref": "23456789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

    def test_prices_0001(self):
        filepath = get_src_path("/tests/data/prices/132.0001.json")
        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)
        pck_filepath = get_src_path("/tests/data/prices/132.0001.pck")

        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

    def test_prices_incorrect_item(self):
        filepath = get_src_path("/tests/data/prices/132.0001_incorrect_item.json")
        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("tests/data/prices/132.0001_incorrect_item.pck")
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

    def test_prices_no_comment(self):
        filepath = get_src_path("tests/data/prices/132.0001_no_comment.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("tests/data/prices/132.0001_no_comment.pck")
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

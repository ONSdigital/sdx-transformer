import unittest

from app.controllers.looped import looping_to_pck
from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from tests.integration.looped import read_submission_data


class TestSPPI(unittest.TestCase):
    def setUp(self):
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "061",
            "period_id": "201605",
            "ru_ref": "23456789012A",
            "form_type": "0011",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

    def test_prices_0011(self):
        filepath = "tests/data/sppi/061.0011_no_change.json"
        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = "tests/data/sppi/061.0011_no_change.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

    def test_prices_both_changed(self):
        filepath = "tests/data/sppi/061.0011_both_changed.json"
        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = "tests/data/sppi/061.0011_both_changed.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

    def test_prices_no_comment(self):
        filepath = "tests/data/sppi/061.0011_no_comment.json"
        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = "tests/data/sppi/061.0011_no_comment.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

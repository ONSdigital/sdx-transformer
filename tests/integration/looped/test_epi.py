import unittest

from app.controllers.looped import looping_to_pck
from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from tests.helpers import get_src_path
from tests.integration.looped import read_submission_data


class TestEPI(unittest.TestCase):

    def setUp(self):
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "133",
            "ru_ref": "12345678901A",
            "period_id": "201605",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "form_type": "0001"
        }

    def test_downstream_epi_full(self):
        """
        Test the downstream transformation for EPI with a full EQ response.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/epi/133.0001_full.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("/tests/data/epi/133.0001_full.pck")

        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

    def test_downstream_epi_no_comments(self):
        """
        Test the downstream transformation for EPI with no comments filled in.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/epi/133.0001_no_comments.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("/tests/data/epi/133.0001_no_comments.pck")

        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

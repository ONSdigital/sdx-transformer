import json
import unittest

from app.definitions import SurveyMetadata, ImageResponse, PCK
from app.pck_managers.looped import get_looping
from tests.integration.looped import read_submission_data


class BresTests(unittest.TestCase):

    def test_to_idbr_pck_no_lu(self):

        filepath = "tests/data/bres/221.0019_no_lu.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0019",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        print("")
        print(actual)

        pck_filepath = "tests/data/bres/221.0019_no_lu.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_0015_to_idbr_pck(self):

        filepath = "tests/data/bres/221.0015.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12345678901A",
            "form_type": "0015",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/bres/221.0015.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_0016_to_idbr_pck(self):

        filepath = "tests/data/bres/221.0016.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12345678901A",
            "form_type": "0016",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/bres/221.0016.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_0017_to_idbr_pck(self):

        filepath = "tests/data/bres/221.0017.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12345678901A",
            "form_type": "0017",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/bres/221.0017.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_0019_to_idbr_pck(self):

        filepath = "tests/data/bres/221.0019.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12345678901A",
            "form_type": "0019",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/bres/221.0019.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

    def test_to_idbr_pck_new_lu(self):

        filepath = "tests/data/bres/221.0019_two_new_lu.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "221",
            "period_id": "201605",
            "ru_ref": "12345678901A",
            "form_type": "0019",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/bres/221.0019_two_new_lu.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)

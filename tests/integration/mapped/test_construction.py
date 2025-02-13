import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class ConstructionPckTests(unittest.TestCase):
    def test_0001_to_pck(self):
        filepath = "tests/data/construction/228.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "48514665167x",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_no_comment_to_pck(self):
        filepath = "tests/data/construction/228.0001.no.comment.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "36114571277k",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.no.comment.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_no_value_to_pck(self):
        filepath = "tests/data/construction/228.0001.no.value.290.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "36115566525A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.no.value.290.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_one_yes_to_pck(self):
        filepath = "tests/data/construction/228.0001.only.one.yes.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "36115566525A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.only.one.yes.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_single_dcode_to_pck(self):
        filepath = "tests/data/construction/228.0001.single.dcode.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "48514665167x",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.single.dcode.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0002_to_pck(self):
        filepath = "tests/data/construction/228.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "14785844082K",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0002.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0002_no_employees_to_pck(self):
        filepath = "tests/data/construction/228.0002.no.employees.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "1605",
            "ru_ref": "14785844082K",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0002.no.employees.nobatch"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0001_different_reporting_period_to_pck(self):
        filepath = "tests/data/construction/228.0001.reporting.period.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "228",
            "period_id": "2401",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_start_date": "2024-01-01",
            "period_end_date": "2024-01-31",
        }
        actual: PCK = get_pck(submission_data, survey_metadata)
        pck_filepath = "tests/data/construction/228.0001.reporting.period.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

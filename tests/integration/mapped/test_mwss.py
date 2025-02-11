import unittest

from app.definitions import PCK, SurveyMetadata
from app.pck_managers.mapped import get_pck, transform, get_build_spec
from tests.integration.mapped import read_submission_data, remove_empties, are_equal


class MWSSTransformTests(unittest.TestCase):

    def test_mwss_minimal(self):
        filepath = "tests/data/mwss/mwss_minimal.json"
        submission_data = read_submission_data(filepath)

        build_spec = get_build_spec("mwss")
        transformed_data = transform(submission_data, build_spec)
        actual = remove_empties(transformed_data)

        expected = {'40': '1', '50': '100', '60': '10', '70': '20', '80': '30', '90': '2', '130': '2', '131': '2',
                    '132': '2', '300': '1'}
        self.assertEqual(expected, actual)

    def test_mwss_full(self):
        filepath = "tests/data/mwss/mwss_full.json"
        submission_data = read_submission_data(filepath)

        build_spec = get_build_spec("mwss")
        transformed_data = transform(submission_data, build_spec)
        actual = remove_empties(transformed_data)

        expected = {'40': '30', '50': '49450', '60': '1300', '70': '1050', '80': '1600', '90': '1', '100': '1',
                    '110': '1', '120': '1', '130': '1', '131': '1', '132': '1',
                    '140': '31', '151': '22000', '152': '56346', '153': '59300', '171': '30', '172': '12', '173': '0',
                    '181': '5000', '182': '700', '183': '0', '190': '1', '200': '1', '210': '1', '220': '1', '300': '1'}
        self.assertEqual(expected, actual)


class MWSSPckTests(unittest.TestCase):

    def test_134_to_pck(self):
        filepath = "tests/data/mwss/134.0005.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "134",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0005",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/mwss/134.0005.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

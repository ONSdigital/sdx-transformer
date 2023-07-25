import json
import unittest

import app.pck
from app.definitions import PCK
from app.pck import get_pck
from tests.integration.pck import TestFormatter, read_submission


class MWSSTests(unittest.TestCase):

    def test_mwss_minimal(self):
        app.pck.formatter_mapping = {
            "COMMON SOFTWARE": TestFormatter
        }

        filepath = "tests/data/mwss/mwss_minimal.json"
        submission_json = read_submission(filepath)

        pck = get_pck(submission_json)
        actual = json.loads(pck)

        expected = {'40': '1', '50': '100', '60': '10', '70': '20', '80': '30', '90': '2', '130': '2', '131': '2',
                    '132': '2', '300': '1'}
        self.assertEqual(expected, actual)

    def test_mwss_full(self):
        app.pck.formatter_mapping = {
            "COMMON SOFTWARE": TestFormatter
        }

        filepath = "tests/data/mwss/mwss_full.json"
        submission_json = read_submission(filepath)

        pck = get_pck(submission_json)
        actual = json.loads(pck)

        expected = {'40': '30', '50': '49450', '60': '1300', '70': '1050', '80': '1600', '90': '1', '100': '1',
                    '110': '1', '120': '1', '130': '1', '131': '1', '132': '1',
                    '140': '31', '151': '22000', '152': '56346', '153': '59300', '171': '30', '172': '12', '173': '0',
                    '181': '5000', '182': '700', '183': '0', '190': '1', '200': '1', '210': '1', '220': '1', '300': '1'}
        self.assertEqual(expected, actual)

    def test_134_to_pck(self):
        filepath = "tests/data/mwss/134.0005.json"
        submission_json = read_submission(filepath)

        actual = get_pck(submission_json)

        pck_filepath = "tests/data/mwss/134.0005.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(expected, actual)

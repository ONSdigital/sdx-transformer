import json
import unittest

import app.pck
from app.definitions import SubmissionJson
from app.formatters.formatter import Formatter
from app.pck import get_pck


class TestFormatter(Formatter):

    def get_pck(self) -> str:
        return json.dumps({str(int(k)): v for k, v in self._data.items() if v is not None})


class MWSSTests(unittest.TestCase):

    def test_mwss_minimal(self):
        app.pck.formatter_mapping = {
            "COMMON SOFTWARE": TestFormatter
        }

        filepath = "tests/data/mwss/mwss_minimal.json"
        with open(filepath) as f:
            submission_json: SubmissionJson = json.load(f)

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
        with open(filepath) as f:
            submission_json: SubmissionJson = json.load(f)

        pck = get_pck(submission_json)
        actual = json.loads(pck)

        expected = {'40': '30', '50': '49450', '60': '1300', '70': '1050', '80': '1600', '90': '1', '100': '1',
                    '110': '150723', '120': '1', '130': '1', '131': '1', '132': '1',
                    '140': '31', '151': '22000', '152': '56346', '153': '59300', '171': '30', '172': '12', '173': '0',
                    '181': '5000', '182': '700', '183': '0', '190': '1', '200': '1', '210': '1', '220': '1', '300': '1'}
        self.assertEqual(expected, actual)

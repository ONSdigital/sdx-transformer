import json
import unittest

import app.manager
from app.definitions import Submission, BuildSpec
from app.formatters.formatter import Formatter
from app.manager import to_submission, get_build_spec, get_pck


class TestFormatter(Formatter):

    def get_pck(self) -> str:
        return json.dumps({str(int(k)): v for k, v in self._data.items() if v is not None})


class PckTests(unittest.TestCase):

    def test_mwss_minimal(self):
        app.manager.formatter_mapping = {
            "COMMON SOFTWARE": TestFormatter
        }

        filepath = "tests/data/mwss_minimal.json"
        with open(filepath) as f:
            submission_json: BuildSpec = json.load(f)

        submission: Submission = to_submission(submission_json)
        build_spec: BuildSpec = get_build_spec(submission)

        pck_name, pck = get_pck(submission, build_spec)
        actual = json.loads(pck)

        expected = {'40': '1', '50': '100', '60': '10', '70': '20', '80': '30', '90': '2', '130': '2', '131': '2',
                    '132': '2', '300': '1'}
        self.assertEqual(expected, actual)

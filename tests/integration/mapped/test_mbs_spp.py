import json
import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data


class MbsSppTests(unittest.TestCase):

    def _run_test(self, form_type: str, period_id: str):
        filepath = f"tests/data/mbs/009.{form_type}.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "009",
            "period_id": period_id,
            "ru_ref": "97148856319Y",
            "form_type": form_type,
            "period_start_date": "2025-03-01",
            "period_end_date": "2025-03-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = f"tests/data/mbs/009.{form_type}-spp.json"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertEqual(json.loads(expected), json.loads(actual))

    def test_0106_to_pck(self):
        self._run_test(form_type="0106", period_id="2503")

    def test_0111_to_pck(self):
        self._run_test(form_type="0111", period_id="2503")

    def test_0255_to_pck(self):
        self._run_test(form_type="0255", period_id="2503")

    def test_0867_to_pck(self):
        self._run_test(form_type="0867", period_id="2503")

import json
import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import JSON
from app.controllers.flat import flat_to_spp
from tests.integration.flat import read_submission_data


class RsiSppTests(unittest.TestCase):

    def _run_test(self, form_type: str, period_id: str):
        filepath = f"tests/data/rsi/023.{form_type}.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "023",
            "period_id": period_id,
            "ru_ref": "97148856319Y",
            "form_type": form_type,
            "period_start_date": "2025-03-01",
            "period_end_date": "2025-03-31",
        }

        actual: JSON = flat_to_spp(submission_data, survey_metadata)

        pck_filepath = f"tests/data/rsi/023.{form_type}-spp.json"
        with open(pck_filepath) as f:
            expected: JSON = f.read()

        self.assertEqual(json.loads(expected), json.loads(actual))

    def test_0106_to_spp(self):
        self._run_test(form_type="0102", period_id="1604")

    def test_0112_to_spp(self):
        self._run_test(form_type="0112", period_id="1604")

    def test_0203_to_spp(self):
        self._run_test(form_type="0203", period_id="1604")

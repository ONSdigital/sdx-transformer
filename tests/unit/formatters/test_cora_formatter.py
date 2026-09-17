import unittest

from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from app.services.formatters.cora_formatter import CoraFormatter
from tests.integration.flat import are_equal


class CoraLoopingFormatterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "001",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

    def test_create_instances(self):
        cora_formatter = CoraFormatter(self.survey_metadata, "YYMM", "YYMM", form_mappings={})

        cora_formatter.create_or_update_instance("0", {"456": "22"})
        cora_formatter.create_or_update_instance("1", {"123": "25"})
        cora_formatter.create_or_update_instance("2", {"123": "49"})

        result: PCK = cora_formatter.create_output()

        expected: PCK = """
001:75553402515:1:201605:1:123:25
001:75553402515:1:201605:2:123:49
001:75553402515:1:201605:0:456:22
"""

        self.assertTrue(are_equal(expected, result))

    def test_create_and_update_instances(self):
        cora_formatter = CoraFormatter(self.survey_metadata, "YYMM", "YYMM", form_mappings={})

        cora_formatter.create_or_update_instance("0", {"456": "22"})
        cora_formatter.create_or_update_instance("1", {"123": "25"})
        cora_formatter.create_or_update_instance("2", {"123": "49"})
        cora_formatter.create_or_update_instance("1", {"345": "99"})

        result: PCK = cora_formatter.create_output()

        expected: PCK = """
001:75553402515:1:201605:1:123:25
001:75553402515:1:201605:2:123:49
001:75553402515:1:201605:1:345:99
001:75553402515:1:201605:0:456:22
"""

        self.assertTrue(are_equal(expected, result))

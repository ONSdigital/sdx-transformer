import unittest

from app.definitions.input import SurveyMetadata, ListCollector
from app.definitions.output import PCK
from app.services.formatters.ppi_looping_formatter import PPILoopingFormatter
from tests.data.prices.ppi_unit_test_data import survey_metadata, original_data


class PPILoopingFormatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.survey_metadata: SurveyMetadata = survey_metadata
        self.original_data: ListCollector = original_data

    def test_create_instances(self):
        ppi_formatter = PPILoopingFormatter("YYMM", "YYMM")

        ppi_formatter.set_original(self.original_data)

        ppi_formatter.create_or_update_instance("1", {"9999": "0", "9997": "200", "9996": "1"}, "uVlxJv")
        ppi_formatter.create_or_update_instance("2", {"9999": "0", "9997": "400", "9996": "1"}, "RiupLc")

        result: PCK = ppi_formatter.generate_pck({"9995": "1"}, self.survey_metadata)
        with open("tests/data/prices/132.0001.pck", "r") as file:
            expected: PCK = file.read()

        self.assertEqual(expected, result)

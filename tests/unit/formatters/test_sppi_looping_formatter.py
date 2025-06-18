import unittest

from app.definitions.input import SurveyMetadata, ListCollector
from app.definitions.output import PCK
from app.services.formatters.sppi_looping_formatter import SPPILoopingFormatter
from tests.data.sppi.sppi_unit_test_data import survey_metadata, original_data


class SPPILoopingFormatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.survey_metadata: SurveyMetadata = survey_metadata
        self.original_data: ListCollector = original_data

    def test_create_instances(self):
        sppi_formatter = SPPILoopingFormatter("YYMM", "YYMM")

        sppi_formatter.set_original(self.original_data)

        sppi_formatter.create_or_update_instance("1", {"9999": "0", "9997": "1000", "9996": "1"}, "TJmMsG")
        sppi_formatter.create_or_update_instance("2", {"9999": "0", "9997": "2000", "9996": "1"}, "RZCIdC")

        result: PCK = sppi_formatter.generate_pck({"9995": "1"}, self.survey_metadata)
        with open("tests/data/sppi/061.0011_no_change.pck", "r") as file:
            expected: PCK = file.read()

        self.assertEqual(expected, result)

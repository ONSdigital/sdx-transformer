import unittest

from app.definitions.output import PCK
from app.services.formatters.formatter import _SurveyMetadata
from app.services.formatters.prices_formatter import PricesFormatter


class PricesFormatterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.survey_metadata: _SurveyMetadata = _SurveyMetadata(
            survey_id = "132",
            period_id = "201605",
            ru_ref = "23456789012A",
            form_type = "0001",
        )

    def test_ppi(self):
        ppi_formatter = PricesFormatter(self.survey_metadata)

        ppi_formatter.create_or_update_instance("0", {"9995": "1"})
        ppi_formatter.create_or_update_instance("12345678901", {"9999": "0", "9997": "200", "9996": "1"})
        ppi_formatter.create_or_update_instance("98765432101", {"9999": "0", "9997": "400", "9996": "1"})

        result: PCK = ppi_formatter.create_output()
        with open("tests/data/prices/132.0001.pck", "r") as file:
            expected: PCK = file.read()

        self.assertEqual(expected, result)

    def test_sppi(self):
        self.survey_metadata.survey_id = "061"

        sppi_formatter = PricesFormatter(self.survey_metadata)

        sppi_formatter.create_or_update_instance("0", {"9995": "1"})
        sppi_formatter.create_or_update_instance("7732015057", {"9999": "0", "9997": "1000", "9996": "1"})
        sppi_formatter.create_or_update_instance("7732016043", {"9999": "0", "9997": "2000", "9996": "1"})

        result: PCK = sppi_formatter.create_output()
        with open("tests/data/sppi/061.0011_no_change.pck", "r") as file:
            expected: PCK = file.read()

        self.assertEqual(expected, result)

import json
import unittest

from app.controllers.prepop import get_prepop
from app.definitions.input import Identifier, PrepopData
from app.definitions.spec import Template


class TestPrices(unittest.TestCase):

    def test_sppi(self):
        self.maxDiff = None

        survey_id = "061"
        input_filepath = "tests/data/sppi/prepop_sppi.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/sppi/prepop_sppi_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)
        self.assertEqual(expected, actual)

    def test_prices_multiple_unit(self):
        self.maxDiff = None

        survey_id = "061"
        input_filepath = "tests/data/sppi/prepop_sppi_multiple_unit.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/sppi/prepop_sppi_multiple_unit_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)
        self.assertEqual(expected, actual)

    def test_prices_full(self):
        self.maxDiff = None

        survey_id = "061"
        input_filepath = "tests/data/sppi/prepop_sppi_full.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/sppi/prepop_sppi_full_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)
        print(actual)
        self.assertEqual(expected, actual)

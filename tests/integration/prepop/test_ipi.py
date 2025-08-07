import json
import unittest

from app.controllers.prepop import get_prepop
from app.definitions.input import PrepopData, Identifier
from app.definitions.spec import Template


class TestIPI(unittest.TestCase):

    def test_ipi(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_ipi_missing_value(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_missing_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_missing_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)
        
    def test_ipi_multiple_items(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_multiple_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_multiple_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)
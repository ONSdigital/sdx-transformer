import json
import unittest

from app.controllers.prepop import get_prepop
from app.definitions.input import Identifier, PrepopData
from app.definitions.spec import Template


class TestEPI(unittest.TestCase):

    def test_epi(self):
        self.maxDiff = None

        survey_id = "133"
        input_filepath = "tests/data/epi/prepop_epi_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/epi/prepop_epi_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_epi_missing_value(self):
        self.maxDiff = None

        survey_id = "133"
        input_filepath = "tests/data/epi/prepop_epi_missing_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/epi/prepop_epi_missing_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_epi_multiple_items(self):
        self.maxDiff = None

        survey_id = "133"
        input_filepath = "tests/data/epi/prepop_epi_multiple_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/epi/prepop_epi_multiple_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

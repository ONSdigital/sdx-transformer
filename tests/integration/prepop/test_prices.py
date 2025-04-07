import json
import unittest

from app.controllers.prepop import get_prepop
from app.definitions.input import Identifier, PrepopData
from app.definitions.spec import Template


class TestPrices(unittest.TestCase):

    def test_prices(self):
        self.maxDiff = None

        survey_id = "132"
        input_filepath = "tests/data/prices/prepop_prices_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/prices/prepop_prices_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        print(f"\n{actual}")

        self.assertEqual(expected, actual)

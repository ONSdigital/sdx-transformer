import json
import unittest

from app.controllers.prepop import get_prepop
from app.definitions.input import Identifier, PrepopData
from app.definitions.spec import Template


class TestASHE(unittest.TestCase):

    def test_ashe(self):
        self.maxDiff = None

        survey_id = "141"
        input_filepath = "tests/data/ashe/prepop_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ashe/prepop_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

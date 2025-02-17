import json
import unittest

from app.definitions.spec import Template
from app.definitions.data import Identifier, PrepopData
from app.controllers.prepop import get_prepop


class BresTest(unittest.TestCase):

    def test_bres(self):

        self.maxDiff = None

        survey_id = "221"
        input_filepath = "tests/data/bres/prepop_bres_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/bres/prepop_bres_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_bres_no_luref(self):

        self.maxDiff = None

        survey_id = "221"
        input_filepath = "tests/data/bres/prepop_bres_input_noluref.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/bres/prepop_bres_output_noluref.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

import json
import unittest

from app.definitions.spec import Template
from app.definitions.input import Identifier, PrepopData
from app.controllers.prepop import get_prepop


class BrsTest(unittest.TestCase):

    def test_brs(self):

        self.maxDiff = None

        survey_id = "241"
        input_filepath = "tests/data/brs/prepop_brs_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/brs/prepop_brs_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        print(actual)

        self.assertEqual(expected, actual)

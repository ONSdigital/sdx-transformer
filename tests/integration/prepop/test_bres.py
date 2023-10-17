import json
import unittest

from app.definitions import PrepopData, Identifier, Template
from app.pck_managers.prepop import get_prepop


class BresTest(unittest.TestCase):

    def test_bres(self):

        survey_id = "221"
        input_filepath = "tests/data/bres/prepop_bres_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/bres/prepop_bres_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        print("\n")
        print(json.dumps(actual))
        self.assertEqual(expected, actual)

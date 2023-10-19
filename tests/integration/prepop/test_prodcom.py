import json
import unittest

from app.definitions import PrepopData, Identifier, Template
from app.pck_managers.prepop import get_prepop


class ProdcomTest(unittest.TestCase):

    def test_prodcom(self):

        self.maxDiff = None

        survey_id = "???"
        input_filepath = "tests/data/prodcom/prepop_prodcom_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/prodcom/prepop_prodcom_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        print("\n")
        print(json.dumps(actual))
        self.assertEqual(expected, actual)

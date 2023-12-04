import json
import unittest

from app.definitions import PrepopData, Identifier, Template
from app.pck_managers.prepop import get_prepop


class MarineTests(unittest.TestCase):

    def test_slate(self):

        survey_id = "076"
        input_filepath = "tests/data/marine/prepop_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/marine/prepop_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

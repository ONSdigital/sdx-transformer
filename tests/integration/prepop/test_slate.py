import json
import unittest

from app.definitions.spec import Template
from app.definitions.input import Identifier, PrepopData
from app.controllers.prepop import get_prepop


class SlateTests(unittest.TestCase):

    def test_slate(self):

        survey_id = "071"
        input_filepath = "tests/data/slate/prepop_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/slate/prepop_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

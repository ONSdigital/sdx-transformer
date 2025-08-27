import json
import unittest

from app.controllers.looped import looping_to_pck
from app.controllers.prepop import get_prepop
from app.definitions.input import Identifier, PrepopData, SurveyMetadata
from app.definitions.output import PCK
from app.definitions.spec import Template
from tests.helpers import get_src_path
from tests.integration.looped import read_submission_data


class TestEPI(unittest.TestCase):

    def setUp(self):
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "133",
            "ru_ref": "12345678901A",
            "ru_name": "ESSENTIAL ENTERPRISE LTD.",
            "trad_as": "ESSENTIAL ENTERPRISE LTD.",
            "period_id": "201605",
            "user_id": "UNKNOWN",
            "ref_p_start_date": "2016-05-01",
            "ref_p_end_date": "2016-05-31",
            "sds_dataset_id": "6f9c40e4-e237-4c94-3ac9-8b802464f2bf",
            "form_type": "0001"
        }

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

    def test_downstream_epi_full(self):
        """
        Test the downstream transformation for EPI with a full EQ response.
        """
        self.maxDiff = None

        survey_id = "133"
        filepath = get_src_path("tests/data/epi/133.0001_full.json")  # TODO better name plz

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        # Write the actual output to a file for inspection
        with open("tests/data/epi/133.0001_full.pck", "w") as f:
            f.write(actual)

        #pck_filepath = get_src_path("/tests/data/epi/132.0001.pck")

        # with open(pck_filepath) as f:
        #     expected: PCK = f.read()
        #
        # self.assertEqual(expected, actual)
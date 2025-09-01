import json
import unittest

from app.controllers.looped import looping_to_pck
from app.controllers.prepop import get_prepop
from app.definitions.input import PrepopData, Identifier, SurveyMetadata
from app.definitions.output import PCK
from app.definitions.spec import Template
from tests.helpers import get_src_path
from tests.integration.looped import read_submission_data


class TestIPI(unittest.TestCase):

    def setUp(self):
        self.survey_metadata: SurveyMetadata = {
            "survey_id": "156",
            "ru_ref": "12345678901A",
            "period_id": "201605",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "form_type": "0001"
        }

    def test_ipi(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_ipi_missing_value(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_missing_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_missing_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_ipi_multiple_items(self):
        self.maxDiff = None

        survey_id = "156"
        input_filepath = "tests/data/ipi/prepop_ipi_multiple_input.json"
        with open(input_filepath) as f:
            prepop_data: PrepopData = json.load(f)

        output_filepath = "tests/data/ipi/prepop_ipi_multiple_output.json"
        with open(output_filepath) as f:
            expected: dict[Identifier: Template] = json.load(f)

        actual = get_prepop(prepop_data, survey_id)

        self.assertEqual(expected, actual)

    def test_downstream_ipi_all_correct(self):
        """
        Test the downstream transformation for IPI where all items are correct and prices are given for them.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/ipi/156.0001_all_correct.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("/tests/data/ipi/156.0001_all_correct.pck")

        with open(pck_filepath) as f:
            expected = f.read()

        self.assertEqual(expected, actual)

    def test_downstream_ipi_no_comments(self):
        """
        Test the downstream transformation for ipi with no comments filled in.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/ipi/156.0001_no_comment.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("tests/data/ipi/156.0001_no_comment.pck")

        with open(pck_filepath) as f:
            expected = f.read()

        self.assertEqual(expected, actual)

    def test_downstream_ipi_incorrect_item(self):
        """
        Test the downstream transformation for IPI where 1 item is incorrect and 1 is correct.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/ipi/156.0001_incorrect_item.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("tests/data/ipi/156.0001_incorrect_item.pck")

        with open(pck_filepath) as f:
            expected = f.read()

        self.assertEqual(expected, actual)

    def test_downstream_ipi_all_incorrect_items(self):
        """
        Test the downstream transformation for IPI where all items are incorrect so no prices are given.
        """
        self.maxDiff = None

        filepath = get_src_path("tests/data/ipi/156.0001_all_incorrect.json")

        submission_data = read_submission_data(filepath)

        actual: PCK = looping_to_pck(submission_data, self.survey_metadata)

        pck_filepath = get_src_path("tests/data/ipi/156.0001_all_incorrect.pck")

        with open(pck_filepath) as f:
            expected = f.read()

        self.assertEqual(expected, actual)

import unittest

from app.controllers.looped import get_looping
from app.definitions.input import SurveyMetadata
from app.definitions.output import PCK
from tests.integration.looped import read_submission_data


class TestPrices(unittest.TestCase):
    def setup(self):
        pass

    def test_prices_0001(self):
        filepath = "tests/data/prices/132.0001.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "132",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        print("")
        print(actual)

        pck_filepath = "tests/data/prices/132.0001.pck"
        with open(pck_filepath, 'rb') as f:
            expected: PCK = f.read().decode()

        # with open(pck_filepath, 'wb') as f:
        #     f.write(actual.encode("utf-8"))

        self.maxDiff = None
        self.assertEqual(expected, actual)
import unittest

from app.definitions import SurveyMetadata, PCK
from app.pck_managers.mapped import get_pck
from tests.integration.mapped import read_submission_data, are_equal


class MbsSppTests(unittest.TestCase):

    def test_0255_to_pck(self):
        pass
        # filepath = "tests/data/mbs/009.0255.json"
        # submission_data = read_submission_data(filepath)
        #
        # survey_metadata: SurveyMetadata = {
        #     "survey_id": "009",
        #     "period_id": "2503",
        #     "ru_ref": "97148856319Y",
        #     "form_type": "0255",
        #     "period_start_date": "2016-05-01",
        #     "period_end_date": "2016-05-31",
        # }
        #
        # actual: PCK = get_pck(submission_data, survey_metadata)
        # print(actual)
        #
        # pck_filepath = "tests/data/mbs/009.0255.pck"
        # with open(pck_filepath) as f:
        #     expected: PCK = f.read()
        #
        # self.assertTrue(are_equal(expected, actual))

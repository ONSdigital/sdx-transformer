import json
import unittest

from app.definitions import SurveyMetadata, PCK, LoopedData
from app.looping import convert_to_looped_data, get_looping
from app.pck import get_pck
from tests.integration.looping import read_submission_data
import pprint

from tests.integration.pck import are_equal


class LoopingTests(unittest.TestCase):

    def test_convert_to_looped_data(self):
        self.maxDiff = None
        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        actual: LoopedData = convert_to_looped_data(submission_data)

        expected: LoopedData = {
            "looped_sections": {
                "people": [
                    {
                        "1": "John",
                        "2": "Doe",
                        "9": "35"
                    },
                    {
                        "1": "Marie",
                        "2": "Doe",
                        "9": "29"
                    },
                ],
                "pets": [
                    {
                        "8": "Dog",  # Pet species
                    },
                ]
            },

            "data_section": {
                "3": "4",  # Number of bedrooms
                "4": "Broadband or WiFi",  # internet-answer
                "5": "A mobile phone network such as 3G, 4G or 5G",
                "6": "Public WiFi hotspot",

                "7.1": "Address Line 1",
                "7.2": "Town",
                "7.3": "NP10 8XG",
                "7.4": "12345678912",
            },

        }

        self.assertEquals(expected, actual)

    def test_looped_to_cora_pck(self):

        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "001",
            "period_id": "201605",
            "ru_ref": "75553402515",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_looping(submission_data, survey_metadata)

        pck_filepath = "tests/data/looping/looping-example-cora.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))
import json
import unittest

from app.definitions.input import SurveyMetadata, LoopedData
from app.definitions.output import SPP, PCK
from app.controllers.looped import convert_to_looped_data, looping_to_pck
from tests.integration.looped import read_submission_data
from tests.integration.flat import are_equal


class LoopingTests(unittest.TestCase):

    def test_convert_to_looped_data(self):
        self.maxDiff = None
        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        actual: LoopedData = convert_to_looped_data(submission_data)

        expected: LoopedData = {
            "looped_sections": {
                "people": {
                    "zGBdpb": {
                        "1": "John",
                        "2": "Doe",
                        "9": "35"
                    },
                    "cWGwcF": {
                        "1": "Marie",
                        "2": "Doe",
                        "9": "29"
                    },
                },
                "pets": {
                    "aTKweq": {
                        "8": "Dog",  # Pet species
                    },
                }
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

        self.assertEqual(expected, actual)

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

        actual: PCK = looping_to_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/looping/looping-example-cora.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_looped_to_spp(self):

        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "999",
            "period_id": "202212",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: SPP = json.loads(looping_to_pck(submission_data, survey_metadata))

        spp_filepath = "tests/data/looping/looping-example-spp.json"
        with open(spp_filepath) as f:
            expected: SPP = json.load(f)

        expected['responses'].sort(key=lambda i: i['instance'])
        actual['responses'].sort(key=lambda i: i['instance'])

        self.assertEqual(expected, actual)

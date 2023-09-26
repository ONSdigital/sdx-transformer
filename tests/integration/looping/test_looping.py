import unittest

from app.definitions import SurveyMetadata, PCK, LoopedData
from app.looping import convert_to_looped_data
from app.pck import get_pck
from tests.integration.looping import read_submission_data


class LoopingTests(unittest.TestCase):

    def test_convert_to_looped_data(self):
        filepath = "tests/data/looping/looping-example.json"
        submission_data = read_submission_data(filepath)

        actual: LoopedData = convert_to_looped_data(submission_data)

        expected: LoopedData = {
            "looped_sections": {
                "people": [
                    {
                        "1": "John",
                        "2": "Doe"
                    },
                    {
                        "1": "Marie",
                        "2": "Doe"
                    },
                ],
                "pets": [
                    {
                        "8": "Dog",  # Pet species
                    },
                ]
            },

            "data": {
                "3": "4",  # Number of bedrooms
                "4": "Broadband or WiFi",  # internet-answer
                "5": "A mobile phone network such as 3G, 4G or 5G",
                "6": "Public WiFi hotspot",

                "7a": "Address Line 1",
                "7b": "Town",
                "7c": "NP10 8XG",
                "7d": "12345678912",
            },

        }

        self.assertEquals(expected, actual)
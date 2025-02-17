import unittest

from app.definitions.data import SurveyMetadata, PCK
from app.definitions.spec import ParseTree
from app.controllers.flat import get_pck
from app.transformers.flat import FlatSpecTransformer
from tests.integration.mapped import read_submission_data, remove_empties, are_equal, get_transformer


class ACASTransformTests(unittest.TestCase):

    def test_negatives_and_missing_comment(self):
        filepath = "tests/data/acas/acas.json"
        submission_data = read_submission_data(filepath)

        transformer: FlatSpecTransformer = get_transformer(
            {
                "survey_id": "171",
                "period_id": "201605",
                "ru_ref": "12346789012A",
                "form_type": "0002",
                "period_start_date": "2016-05-01",
                "period_end_date": "2016-05-31",
            },
        )
        parse_tree: ParseTree = transformer.interpolate()
        transformed_data = transformer.run(parse_tree, submission_data)
        actual = remove_empties(transformed_data)

        expected = {
            "146": "2",
            "150": "-3",
            "151": "24",
            "152": "20",
            "153": "5",
            "154": "72",
            "155": "28",
            "156": "12",
            "157": "2",
            "158": "101",
            "159": "21",
            "160": "43",
            "161": "10",
            "162": "2",
            "163": "13",
            "164": "22",
            "165": "35",
            "166": "32",
            "167": "54",
            "168": "32",
            "169": "12",
            "170": "23",
            "171": "43",
            "172": "22",
            "173": "2",
            "174": "2",
            "175": "188",
            "176": "178",
            "200": "12",
            "201": "22",
            "202": "16",
            "203": "46",
            "204": "5",
            "205": "0",
            "206": "5",
            "207": "1",
            "208": "56",
            "209": "23",
            "210": "12",
            "211": "55",
            "212": "0",
            "213": "0",
            "214": "0",
            "215": "0",
            "218": "5",
            "219": "7",
            "220": "0",
            "221": "1",
            "222": "2",
            "223": "163",
            "224": "103",
            "225": "1",
            "226": "54",
            "227": "66",
            "228": "2",
            "231": "2",
            "234": "2",
            "237": "2",
            "238": "54",
            "239": "66",
            "300": "54",
            "301": "12",
            "302": "12",
            "303": "0",
            "304": "1",
            "305": "0",
            "306": "1",
            "307": "0",
            "308": "1",
            "309": "0",
            "310": "0",
            "311": "0",
            "312": "2",
            "313": "69",
            "314": "12",
            "315": "56",
            "316": "78",
            "317": "0",
            "318": "0",
            "319": "0",
            "320": "0",
            "321": "0",
            "322": "0",
            "323": "2",
            "324": "56",
            "325": "78",
            "400": "5",
            "401": "0",
            "402": "22",
            "403": "13",
            "404": "8",
            "405": "31",
            "406": "1",
            "407": "0",
            "408": "11",
            "409": "0",
            "410": "1",
            "411": "0",
            "412": "1",
            "413": "0",
            "414": "0",
            "415": "0",
            "416": "2",
            "417": "0",
            "418": "0",
            "419": "0",
            "420": "0",
            "421": "0",
            "422": "2",
            "423": "51",
            "424": "44",
            "500": "4",
            "501": "6",
            "502": "22",
            "503": "12",
            "504": "3",
            "505": "9",
            "506": "79",
            "507": "22",
            "508": "46",
            "509": "6",
            "510": "66",
            "511": "7",
            "512": "1",
            "513": "0",
            "514": "12",
            "515": "7",
            "516": "4",
            "517": "0",
            "518": "0",
            "519": "1",
            "520": "2",
            "521": "237",
            "522": "70",
            "601": "5",
            "602": "1",
            "603": "8",
            "604": "7",
            "605": "22",
            "606": "7",
            "607": "233",
            "608": "46",
            "609": "1",
            "610": "0",
            "611": "12",
            "612": "0",
            "613": "4",
            "614": "1",
            "615": "7",
            "616": "1",
            "617": "74",
            "618": "7",
            "619": "2",
            "620": "366",
            "621": "70",
            "700": "7",
            "701": "1",
            "702": "10",
            "703": "0",
            "704": "6",
            "705": "1",
            "706": "12",
            "707": "1",
            "708": "1",
            "709": "0",
            "710": "1",
            "711": "0",
            "712": "0",
            "713": "0",
            "714": "1",
            "715": "0",
            "716": "2",
            "717": "38",
            "718": "3",
            "800": "7",
            "801": "0",
            "802": "8",
            "803": "1",
            "804": "4",
            "805": "1",
            "806": "8",
            "807": "1",
            "808": "2",
            "809": "27",
            "810": "3",
            "811": "1",
            "812": "77",
            "813": "1",
            "814": "1",
            "815": "7",
            "816": "0",
            "817": "2",
            "820": "2",
            "823": "2",
            "826": "2",
            "829": "2",
            "830": "84",
            "831": "1",
            "900": "2",
            "901": "54",
            "902": "1",
            "903": "2",
            "904": "8",
            "905": "6",
        }

        self.assertEqual(expected, actual)


class ACASPckTests(unittest.TestCase):

    def test_0002_to_pck(self):
        filepath = "tests/data/acas/171.0002.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "171",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0002",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/acas/171.0002.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

    def test_0003_to_pck(self):
        filepath = "tests/data/acas/171.0003.json"
        submission_data = read_submission_data(filepath)

        survey_metadata: SurveyMetadata = {
            "survey_id": "171",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0003",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual: PCK = get_pck(submission_data, survey_metadata)

        pck_filepath = "tests/data/acas/171.0003.pck"
        with open(pck_filepath) as f:
            expected: PCK = f.read()

        self.assertTrue(are_equal(expected, actual))

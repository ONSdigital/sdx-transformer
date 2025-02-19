import json
import unittest

from app.services.berd.collect_items import collect_list_items
from app.services.berd.convert_data import extract_answers, convert_to_spp
from app.services.berd.definitions import Answer, SPP
from app.definitions.input import SurveyMetadata
from app.controllers.looped import get_looping


class BERDTransformerTests(unittest.TestCase):

    def test_full_transform(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a2", "value": "No", "list_item_id": "aaa"},
                {"answer_id": "a3", "value": "Yes", "list_item_id": "aaa"},
                {"answer_id": "a4", "value": "No", "list_item_id": "aaa"},
                {"answer_id": "a5", "value": "Yes", "list_item_id": "bbb"},
                {"answer_id": "a6", "value": "No", "list_item_id": "bbb"},
                {"answer_id": "a7", "value": "Yes", "list_item_id": "ccc"},
                {"answer_id": "a8", "value": "No", "list_item_id": "ccc"},
                {"answer_id": "a9", "value": "x"},
                {"answer_id": "a10", "value": "y"},
                {"answer_id": "a11", "value": "x"},
                {"answer_id": "a12", "value": "y"},
                {"answer_id": "a13", "value": "x"},
                {"answer_id": "a14", "value": "y"},
            ],
            "lists": [
                {"items": ["aaa", "bbb"], "name": "product1"},
                {"items": ["ccc"], "name": "product2"},
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "c101"},
                {"answer_id": "a2", "code": "c102"},
                {"answer_id": "a3", "code": "d101"},
                {"answer_id": "a4", "code": "d102"},
                {"answer_id": "a5", "code": "c101"},
                {"answer_id": "a6", "code": "c102"},
                {"answer_id": "a7", "code": "c103"},
                {"answer_id": "a8", "code": "c104"},
                {"answer_id": "a9", "code": "105"},
                {"answer_id": "a10", "code": "106"},
                {"answer_id": "a11", "code": "56e107"},
                {"answer_id": "a12", "code": "56e108"},
                {"answer_id": "a13", "code": "56f107"},
                {"answer_id": "a14", "code": "56f108"},
            ]
        }

        survey_metadata: SurveyMetadata = {
            "survey_id": "002",
            "period_id": "202212",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
        }

        actual = get_looping(data, survey_metadata)

        expected = {
            'formtype': '0001',
            'reference': '12346789012',
            'period': '202212',
            'survey': '002',
            'responses': [
                {'questioncode': '101', 'response': 'Yes', 'instance': 1},
                {'questioncode': '102', 'response': 'No', 'instance': 1},
                {'questioncode': '101', 'response': 'Yes', 'instance': 2},
                {'questioncode': '102', 'response': 'No', 'instance': 2},
                {'questioncode': '101', 'response': 'Yes', 'instance': 3},
                {'questioncode': '102', 'response': 'No', 'instance': 3},
                {'questioncode': '103', 'response': 'Yes', 'instance': 1},
                {'questioncode': '104', 'response': 'No', 'instance': 1},
                {'questioncode': '105', 'response': 'x', 'instance': 0},
                {'questioncode': '106', 'response': 'y', 'instance': 0},
                {'questioncode': '107', 'response': 'x', 'instance': 1},
                {'questioncode': '108', 'response': 'y', 'instance': 1},
                {'questioncode': '107', 'response': 'x', 'instance': 2},
                {'questioncode': '108', 'response': 'y', 'instance': 2}
            ]
        }

        self.assertEqual(expected, json.loads(actual))

    def test_extract_answers(self):
        data = {
            "answers": [
                {"answer_id": "q1", "value": "Yes, I can report for this period"},
                {"answer_id": "a1", "value": "Civil Research and Development", "list_item_id": "qObPqR"},
                {"answer_id": "a1", "value": "Defence Research and Development", "list_item_id": "Uztndf"},
                {"answer_id": "a1", "value": "Both, civil and defence Research and Development",
                 "list_item_id": "GjDKpD"},
                {"answer_id": "a6", "value": "1 - Agriculture", "list_item_id": "qObPqR"},
                {"answer_id": "a6", "value": "2 - Mining and quarrying", "list_item_id": "Uztndf"},
                {"answer_id": "a6", "value": "3 - Food products and beverages", "list_item_id": "GjDKpD"},
                {"answer_id": "a2", "value": 10000, "list_item_id": "qObPqR"},
                {"answer_id": "a2", "value": 5000, "list_item_id": "GjDKpD"},
                {"answer_id": "a3", "value": 5000, "list_item_id": "qObPqR"},
                {"answer_id": "a3", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a4", "value": 1000, "list_item_id": "Uztndf"},
                {"answer_id": "a4", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a5", "value": 500, "list_item_id": "Uztndf"},
                {"answer_id": "a5", "value": 1000, "list_item_id": "GjDKpD"}
            ],
            "lists": [
                {"items": ["qObPqR", "Uztndf", "GjDKpD"], "name": "product_codes"},
                {"items": ["ebQYeQ", "ImViOn"], "name": "product_codes_2"}
            ],
            "answer_codes": [
                {"answer_id": "q1", "code": "101"},
                {"answer_id": "a1", "code": "200"},
                {"answer_id": "a6", "code": "201"},
                {"answer_id": "a2", "code": "c202"},
                {"answer_id": "a3", "code": "c203"},
                {"answer_id": "a4", "code": "d202"},
                {"answer_id": "a5", "code": "d203"}
            ]
        }

        expected = [
            Answer(qcode='101', value='Yes, I can report for this period', list_item_id=None, group=None),
            Answer(qcode='200', value='Civil Research and Development', list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='200', value='Defence Research and Development', list_item_id='Uztndf', group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='GjDKpD',
                   group='product_codes'),
            Answer(qcode='201', value='1 - Agriculture', list_item_id='qObPqR', group='product_codes'),
            Answer(qcode='201', value='2 - Mining and quarrying', list_item_id='Uztndf', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='GjDKpD', group='product_codes'),
            Answer(qcode='c202', value='10000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c202', value='5000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='c203', value='5000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c203', value='3000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='d202', value='1000', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d202', value='3000', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='d203', value='500', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d203', value='1000', list_item_id='dGjDKpD', group='product_codes')]

        actual = extract_answers(data)
        self.assertEqual(expected, actual)

    def test_collected_list_items(self):
        answer_list = [
            Answer(qcode='101', value='Yes, I can report for this period', list_item_id=None, group=None),
            Answer(qcode='200', value='Civil Research and Development', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='200', value='Defence Research and Development', list_item_id='dUztndf',
                   group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='cGjDKpD',
                   group='product_codes'),
            Answer(qcode='200', value='Both, civil and defence Research and Development', list_item_id='dGjDKpD',
                   group='product_codes'),
            Answer(qcode='201', value='1 - Agriculture, hunting and forestry; fishing', list_item_id='cqObPqR',
                   group='product_codes'),
            Answer(qcode='201', value='2 - Mining and quarrying (including solids, liquids and gases)',
                   list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='201', value='3 - Food products and beverages', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='c202', value='10000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c202', value='5000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='c203', value='5000', list_item_id='cqObPqR', group='product_codes'),
            Answer(qcode='c203', value='3000', list_item_id='cGjDKpD', group='product_codes'),
            Answer(qcode='d202', value='1000', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d202', value='3000', list_item_id='dGjDKpD', group='product_codes'),
            Answer(qcode='d203', value='500', list_item_id='dUztndf', group='product_codes'),
            Answer(qcode='d203', value='1000', list_item_id='dGjDKpD', group='product_codes')
        ]

        expected = [
            SPP(questioncode='101', response='Yes, I can report for this period', instance=0),
            SPP(questioncode='200', response='Civil Research and Development', instance=1),
            SPP(questioncode='200', response='Defence Research and Development', instance=2),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=3),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=4),
            SPP(questioncode='201', response='1 - Agriculture, hunting and forestry; fishing', instance=1),
            SPP(questioncode='201', response='2 - Mining and quarrying (including solids, liquids and gases)',
                instance=2),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=3),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=4),
            SPP(questioncode='c202', response='10000', instance=1),
            SPP(questioncode='c202', response='5000', instance=3),
            SPP(questioncode='c203', response='5000', instance=1),
            SPP(questioncode='c203', response='3000', instance=3),
            SPP(questioncode='d202', response='1000', instance=2),
            SPP(questioncode='d202', response='3000', instance=4),
            SPP(questioncode='d203', response='500', instance=2),
            SPP(questioncode='d203', response='1000', instance=4)
        ]

        actual = convert_to_spp(answer_list)
        self.assertEqual(expected, actual)

    def test_full_example(self):
        data = {
            "answers": [
                {"answer_id": "a1", "value": "Civil Research and Development", "list_item_id": "qObPqR"},
                {"answer_id": "a1", "value": "Defence Research and Development", "list_item_id": "Uztndf"},
                {"answer_id": "a1", "value": "Both, civil and defence Research and Development",
                 "list_item_id": "GjDKpD"},
                {"answer_id": "a6", "value": "1 - Agriculture, hunting and forestry; fishing",
                 "list_item_id": "qObPqR"},
                {"answer_id": "a6", "value": "2 - Mining and quarrying (including solids, liquids and gases)",
                 "list_item_id": "Uztndf"},
                {"answer_id": "a6", "value": "3 - Food products and beverages", "list_item_id": "GjDKpD"},
                {"answer_id": "a2", "value": 10000, "list_item_id": "qObPqR"},
                {"answer_id": "a2", "value": 5000, "list_item_id": "GjDKpD"},
                {"answer_id": "a3", "value": 5000, "list_item_id": "qObPqR"},
                {"answer_id": "a3", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a4", "value": 1000, "list_item_id": "Uztndf"},
                {"answer_id": "a4", "value": 3000, "list_item_id": "GjDKpD"},
                {"answer_id": "a5", "value": 500, "list_item_id": "Uztndf"},
                {"answer_id": "a5", "value": 1000, "list_item_id": "GjDKpD"}
            ],
            "lists": [
                {"items": ["qObPqR", "Uztndf", "GjDKpD"], "name": "product_codes"},
                {"items": ["ebQYeQ", "ImViOn"], "name": "product_codes_2"}
            ],
            "answer_codes": [
                {"answer_id": "a1", "code": "200"},
                {"answer_id": "a6", "code": "201"},
                {"answer_id": "a2", "code": "c202"},
                {"answer_id": "a3", "code": "c203"},
                {"answer_id": "a4", "code": "d202"},
                {"answer_id": "a5", "code": "d203"}
            ]
        }

        expected = [
            SPP(questioncode='200', response='Civil Research and Development', instance=1),
            SPP(questioncode='200', response='Defence Research and Development', instance=2),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=3),
            SPP(questioncode='200', response='Both, civil and defence Research and Development', instance=4),
            SPP(questioncode='201', response='1 - Agriculture, hunting and forestry; fishing', instance=1),
            SPP(questioncode='201', response='2 - Mining and quarrying (including solids, liquids and gases)',
                instance=2),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=3),
            SPP(questioncode='201', response='3 - Food products and beverages', instance=4),
            SPP(questioncode='c202', response='10000', instance=1),
            SPP(questioncode='c202', response='5000', instance=3),
            SPP(questioncode='c203', response='5000', instance=1),
            SPP(questioncode='c203', response='3000', instance=3),
            SPP(questioncode='d202', response='1000', instance=2),
            SPP(questioncode='d202', response='3000', instance=4),
            SPP(questioncode='d203', response='500', instance=2),
            SPP(questioncode='d203', response='1000', instance=4)
        ]

        actual = convert_to_spp(collect_list_items(extract_answers(data)))

        self.assertEqual(expected, actual)

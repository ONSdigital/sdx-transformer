import json
import unittest

from app import sdx_app
from app.routes import init_routes


class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the SDX app
        init_routes(sdx_app)

        # Create a test client for our SDX app
        cls.client = sdx_app.app.test_client()

    def test_process_prepop_without_json(self):

        # Define some invalid data in the body
        data = None

        # Define query parameters
        query_params = {
            'survey_id': '123',
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/prepop',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Data is not in json format'})

    def test_prepop_with_bad_json(self):

        # Define some json as a top level list
        data = [
            {"Item1": "Hi"}
        ]

        # Define a valid survey id
        query_params = {
            'survey_id': '066',
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/prepop',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Prepop data is not in correct format'})

    def test_process_prepop_without_a_survey_id(self):
        # Define some valid json
        data = {
            "item1": "value1"
        }

        # Define empty query params
        query_params = {}

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/prepop',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Missing survey id from request'})

    def test_process_pck_without_survey_id(self):
        # Define some valid json
        data = {
            "item1": "value1"
        }

        # Define query params, without survey ID
        query_params = {
            "period_id": "123",
            "ru_ref": "123",
            "form_type": "123",
            "period_start_date": "123",
            "period_end_date": "123",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/pck',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Missing required parameter survey_id from request'})

    def test_process_pck_with_invalid_format_version_01(self):
        # Define some valid json
        data = None

        # Define valid query params
        query_params = {
            "survey_id": "123",
            "period_id": "123",
            "ru_ref": "123",
            "form_type": "123",
            "period_start_date": "123",
            "period_end_date": "123",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/pck',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual({'Unrecoverable error': 'Submission data is not in json format'}, response_json)

    def test_process_pck_with_invalid_format_version_03(self):
        # Define some valid json
        data = None

        # Define valid query params
        query_params = {
            "survey_id": "123",
            "period_id": "123",
            "ru_ref": "123",
            "form_type": "123",
            "period_start_date": "123",
            "period_end_date": "123",
            "data_version": "0.0.3",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/pck',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(400, response.status_code)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual({'Unrecoverable error': 'Submission data is not in json format'}, response_json)

    def test_pck_happy_path(self):

        # Define some valid json
        data = {
            "50": "100",
            "60": "110",
            "146": "This is another comment",
            "551": "33",
            "552": "44",
            "553": "55",
            "554": "66",
            "561": "44",
            "562": "66",
            "651": "33",
            "652": "44",
            "653": "55",
            "654": "66",
            "661": "44",
            "662": "66"
        }

        # Define valid query params for 169.0003
        query_params = {
            "survey_id": "169",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0003",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "data_version": "0.0.1",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/pck',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert a 200
        self.assertEqual(200, response.status_code)

    def test_prepop_happy_path(self):

        # Define some valid json
        data = {
            "10000000000": [
                {
                    "ruref": "10000000000",
                    "luref": "1000000",
                    "luname1": "STUBBS BUILDING PRODUCTS LTD",
                    "luname2": "",
                    "luname3": "",
                    "luaddr1": "WELLINGTON ROAD",
                    "luaddr2": "LOCHMABEN",
                    "luaddr3": "SWINDON",
                    "luaddr4": "BEDS",
                    "luaddr5": "GLOS",
                    "lupostcode": "DE41 2WA",
                    "formtype": "01"
                }
            ],
            "20000000000": [
                {
                    "ruref": "20000000000",
                    "luref": "2000000",
                    "luname1": "TUBBS",
                    "luname2": "BATHROOM",
                    "luname3": "PRODUCTS",
                    "luaddr1": "IVORY ROAD",
                    "luaddr2": "SNOWDONIA",
                    "luaddr3": "WINDON",
                    "luaddr4": "BEDS",
                    "luaddr5": "HAMP",
                    "lupostcode": "HA41 2WA",
                    "formtype": "02"
                },
                {
                    "ruref": "20000000000",
                    "luref": "2000001",
                    "luname1": "TUBBS BATHROOM PRODUCTS",
                    "luname2": "LTD",
                    "luname3": "",
                    "luaddr1": "HAPPY STREET",
                    "luaddr2": "CORNWALL",
                    "luaddr3": "RUNDON",
                    "luaddr4": "BEDS",
                    "luaddr5": "GLOS",
                    "lupostcode": "GL2X 5EF",
                    "formtype": "02"
                },
                {
                    "ruref": "20000000000",
                    "luref": "2000002",
                    "luname1": "TUBBS BATHROOM PRODUCTS",
                    "luname2": "AND CO",
                    "luname3": "",
                    "luaddr1": "GRACE ROAD",
                    "luaddr2": "DEVON",
                    "luaddr3": "HAPPY",
                    "luaddr4": "BEDS",
                    "luaddr5": "GLOS",
                    "lupostcode": "DE41 2XJ",
                    "formtype": "02"
                }
            ]
        }

        # Define valid query params for 066
        query_params = {
            "survey_id": "066",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/prepop',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert a 200
        self.assertEqual(200, response.status_code)

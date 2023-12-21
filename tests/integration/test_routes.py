import json
import unittest

from app import sdx_app
from app.routes import init_routes


class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the SDX app
        init_routes(sdx_app)

        # Create a test client for our SDX app
        self.client = sdx_app.app.test_client()

    def test_process_prepop_with_invalid_json(self):

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
        self.assertEqual(response.status_code, 400)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Data is not in json format'})

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
        self.assertEqual(response.status_code, 400)

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
            "period_end_date":"123",
        }

        # Send a POST request with JSON body and query parameters
        response = self.client.post('/pck',
                                    data=json.dumps(data),
                                    query_string=query_params,
                                    content_type='application/json')

        # Assert the HTTP status code (BAD request)
        self.assertEqual(response.status_code, 400)

        # Assert the kind of error
        response_json = response.json
        self.assertEqual(response_json, {'Unrecoverable error': 'Missing required parameter survey_id from request'})

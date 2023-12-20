import json
import unittest

from sdx_gcp.errors import DataError, UnrecoverableError

from app import sdx_app
from app.routes import init_routes


class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Set up the SDX app
        init_routes(sdx_app)

        # Create a test client for our SDX app
        self.client = sdx_app.app.test_client()

    def test_process_prepop_with_invalid_json(self):
        # Define the data to be sent in the request body
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


import unittest
from app import sdx_app


class TestRoutes(unittest.TestCase):

    def setUp(self):
        # Create a test client for our SDX app
        self.client = sdx_app.app.test_client()

    def test_process_pck_with_invalid_json(self):
        pass


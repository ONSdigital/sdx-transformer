import json
import os
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sdx_base.run import run
from sdx_base.settings.app import AppSettings

from app.routes import router
from tests.helpers import get_src_path
from tests.integration.looped import read_submission_data


class TestRoutes(unittest.TestCase):

    def setUp(self):
        os.environ["PROJECT_ID"] = "my-project"
        proj_root = Path(__file__).parent.parent.parent  # sdx-deliver dir

        app: FastAPI = run(AppSettings,
                           routers=[router],
                           proj_root=proj_root,
                           serve=lambda a, b: a
                           )

        self.client = TestClient(app)

    def test_process_pck(self):
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
            "tx_id": "123",
            "survey_id": "169",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0003",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "data_version": "0.0.1",
        }

        response = self.client.post("/pck",
                                        data=json.dumps(data),
                                        params=query_params)

        self.assertEqual(200, response.status_code)

    def test_process_pck_looping(self):
        filepath = get_src_path("tests/data/ipi/156.0001_all_correct.json")
        data = read_submission_data(filepath)

        query_params = {
            "tx_id": "123",
            "survey_id": "156",
            "ru_ref": "12345678901A",
            "form_type": "0001",
            "period_id": "201605",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "data_version": "0.0.3"
        }

        response = self.client.post("/pck",
                                    data=json.dumps(data),
                                    params=query_params)

        self.assertEqual(200, response.status_code)

    def test_process_spp(self):
        filepath = "tests/data/berd/002.0001.json"
        data = read_submission_data(filepath)

        query_params = {
            "tx_id": "123",
            "survey_id": "002",
            "period_id": "201605",
            "ru_ref": "12346789012A",
            "form_type": "0001",
            "period_start_date": "2016-05-01",
            "period_end_date": "2016-05-31",
            "data_version": "0.0.3"
        }

        response = self.client.post("/spp",
                                    data=json.dumps(data),
                                    params=query_params)

        self.assertEqual(200, response.status_code)

    def test_process_prepop(self):
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
            "tx_id": "123",
            "survey_id": "066",
        }

        response = self.client.post("/prepop",
                                    data=json.dumps(data),
                                    params=query_params)

        self.assertEqual(200, response.status_code)

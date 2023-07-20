from sdx_gcp import Request, Flask, TX_ID
from sdx_gcp.errors import DataError

from app.definitions import SubmissionJson, PrepopData, Identifier, Template
from app.pck import get_pck
from app.prepop import get_prepop


def process_pck(req: Request, tx_id: TX_ID):
    submission_json: SubmissionJson = req.get_json(force=True, silent=True)
    if submission_json is None:
        raise DataError("Submission is not in json format")

    pck: str = get_pck(submission_json)
    response: Flask.Response = Flask.make_response(pck, 200)
    response.mimetype = "text/plain"
    return response


def process_prepop(req: Request, tx_id: TX_ID):
    prepop_data: PrepopData = req.get_json(force=True, silent=True)
    survey_id: str = req.args.get("survey_id")

    if prepop_data is None:
        raise DataError("Data is not in json format")

    if survey_id is None:
        raise DataError("Missing survey id from request")

    result: dict[Identifier: Template] = get_prepop(survey_id, prepop_data)
    return Flask.jsonify(result)

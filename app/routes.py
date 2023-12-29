from sdx_gcp import Request, Flask, TX_ID
from sdx_gcp.app import get_logger, SdxApp
from sdx_gcp.errors import DataError

from app.definitions import PrepopData, Identifier, Template, PCK, Data, SurveyMetadata, ListCollector
from app.pck_managers.looped import get_looping
from app.pck_managers.mapped import get_pck
from app.pck_managers.prepop import get_prepop


logger = get_logger()


def process_pck(req: Request, _tx_id: TX_ID):
    logger.info("Received pck request")

    survey_metadata: SurveyMetadata = {
        "survey_id": req.args.get("survey_id", ""),
        "period_id": req.args.get("period_id", ""),
        "ru_ref": req.args.get("ru_ref", ""),
        "form_type": req.args.get("form_type", ""),
        "period_start_date": req.args.get("period_start_date", ""),
        "period_end_date": req.args.get("period_end_date", ""),
    }

    logger.info("Received Parameters", **survey_metadata)

    for k, v in survey_metadata.items():
        if v == "":
            raise DataError(f"Missing required parameter {k} from request")

    data_version: str = req.args.get("data_version", "0.0.1")

    if data_version == "0.0.3":
        submission_data: ListCollector = req.get_json(force=True, silent=True)
        if submission_data is None:
            raise DataError("Submission data is not in json format")
        pck: PCK = get_looping(submission_data, survey_metadata)
    else:
        submission_data: Data = req.get_json(force=True, silent=True)
        if submission_data is None:
            raise DataError("Submission data is not in json format")
        pck: PCK = get_pck(submission_data, survey_metadata)

    response: Flask.Response = Flask.make_response(pck, 200)
    response.mimetype = "text/plain"
    return response


def process_prepop(req: Request, _tx_id: TX_ID):
    logger.info("Received prepop request")
    prepop_data: PrepopData = req.get_json(force=True, silent=True)
    survey_id: str = req.args.get("survey_id")

    if prepop_data is None:
        raise DataError("Data is not in json format")

    if survey_id is None:
        raise DataError("Missing survey id from request")

    result: dict[Identifier: Template] = get_prepop(prepop_data, survey_id)
    return Flask.jsonify(result)


def init_routes(app: SdxApp):
    app.add_post_endpoint(process_pck, rule="/pck")
    app.add_post_endpoint(process_prepop, rule="/prepop")

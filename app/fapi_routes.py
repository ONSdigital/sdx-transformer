from fastapi import FastAPI, Request, Response
from sdx_gcp import TX_ID
from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import PrepopData, Identifier, Template, SurveyMetadata, ListCollector, PCK, Data
from app.pck_managers.looped import get_looping
from app.pck_managers.mapped import get_pck
from app.pck_managers.prepop import get_prepop

app = FastAPI()

logger = get_logger()


@app.post("/pck")
async def process_pck(request: Request, _tx_id: TX_ID):
    logger.info("Received pck request")
    logger.info(f"Request body: {request.json()}")

    survey_metadata: SurveyMetadata = {
        "survey_id": request.query_params.get("survey_id", ""),
        "period_id": request.query_params.get("period_id", ""),
        "ru_ref": request.query_params.get("ru_ref", ""),
        "form_type": request.query_params.get("form_type", ""),
        "period_start_date": request.query_params.get("period_start_date", ""),
        "period_end_date": request.query_params.get("period_end_date", ""),
    }

    logger.info("Received Parameters", **survey_metadata)

    use_image_formatter: bool = request.query_params.get("use_image_formatter", "False").upper() == "TRUE"

    if use_image_formatter:
        logger.info("Using image transformer")
    else:
        logger.info("NOT using image transformer")

    for k, v in survey_metadata.items():
        if v == "":
            raise DataError(f"Missing required parameter {k} from request")

    data_version: str = request.query_params.get("data_version", "0.0.1")

    if data_version == "0.0.3":
        submission_data: ListCollector = request.json(force=True, silent=True)
        if submission_data is None:
            raise DataError("Submission data is not in json format")

        pck: PCK = get_looping(submission_data, survey_metadata, use_image_formatter=use_image_formatter)

    else:
        submission_data: Data = request.json(force=True, silent=True)
        if submission_data is None:
            raise DataError("Submission data is not in json format")
        pck: PCK = get_pck(submission_data, survey_metadata)

    return Response(content=PCK, mimetype="text/plain", status=200)


@app.post("/prepop")
async def process_prepop(request: Request, _tx_id: TX_ID):
    logger.info("Received prepop request")
    try:
        prepop_data = await request.json()
    except ValueError:
        prepop_data = None
    if prepop_data is None:
        return {"message": "No JSON data or invalid JSON"}

    survey_id: str = request.query_params.get("survey_id")

    if prepop_data is None:
        raise DataError("Data is not in json format")

    if survey_id is None:
        raise DataError("Missing survey id from request")

    result: dict[Identifier: Template] = get_prepop(prepop_data, survey_id)
    # FastAPI turns result to JSON under the hood
    return result


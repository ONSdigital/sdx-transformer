import json
from collections.abc import Callable

from fastapi import APIRouter
from sdx_base.errors.errors import DataError
from starlette.responses import JSONResponse, PlainTextResponse

from app import get_logger
from app.controllers.flat import flat_to_spp, flat_to_pck
from app.controllers.looped import looping_to_spp, looping_to_pck
from app.definitions.output import PCK, JSON
from app.definitions.spec import Template
from app.definitions.input import Data, SurveyMetadata, Identifier, PrepopData, ListCollector
from app.controllers.prepop import get_prepop

logger = get_logger()
router = APIRouter()

looping_processor = Callable[[ListCollector, SurveyMetadata], str]
flat_processor = Callable[[dict[str, str], SurveyMetadata], str]


@router.post("/pck")
async def process_pck(survey_id: str,
                      period_id: str,
                      ru_ref: str,
                      form_type: str,
                      period_start_date: str,
                      period_end_date: str,
                      data_version: str,
                      data: dict) -> PlainTextResponse:
    """Process a request to convert submission data to a PCK file."""
    logger.info("Received pck request")

    metadata: SurveyMetadata = {
        "survey_id": survey_id,
        "period_id": period_id,
        "ru_ref": ru_ref,
        "form_type": form_type,
        "period_start_date": period_start_date,
        "period_end_date": period_end_date,
        "data_version": data_version
    }

    result: PCK = _process(data, metadata, looping_to_pck, flat_to_pck)
    return PlainTextResponse(content=result, status_code=200)


@router.post("/spp")
async def process_spp(survey_id: str,
                      period_id: str,
                      ru_ref: str,
                      form_type: str,
                      period_start_date: str,
                      period_end_date: str,
                      data_version: str,
                      data: dict) -> JSONResponse:
    """Process a request to convert submission data to a SPP file."""
    logger.info("Received spp request")

    metadata: SurveyMetadata = {
        "survey_id": survey_id,
        "period_id": period_id,
        "ru_ref": ru_ref,
        "form_type": form_type,
        "period_start_date": period_start_date,
        "period_end_date": period_end_date,
        "data_version": data_version
    }
    result: JSON = _process(data, metadata, looping_to_spp, flat_to_spp)
    return JSONResponse(content=json.loads(result), status_code=200)


def _process(submission_data: dict,
             survey_metadata: SurveyMetadata,
             process_looping: looping_processor,
             process_flat: flat_processor) -> str:

    data_version: str = survey_metadata["data_version"] if "data_version" in survey_metadata else "0.0.1"
    result: str

    if data_version == "0.0.3":
        list_data: ListCollector = submission_data
        if list_data is None:
            raise DataError("Submission data is not in json format")

        result = process_looping(list_data, survey_metadata)

    else:
        map_data: Data = submission_data
        if map_data is None:
            raise DataError("Submission data is not in json format")
        result = process_flat(map_data, survey_metadata)

    return result


@router.post("/prepop")
async def process_prepop(prepop_data: PrepopData, survey_id: str) -> JSONResponse:
    """Process a request to convert pre-population data into supplementary format."""

    logger.info("Received prepop request")

    if prepop_data is None:
        raise DataError("Data is not in json format")

    if survey_id is None:
        raise DataError("Missing survey id from request")

    result: dict[Identifier, Template] = get_prepop(prepop_data, survey_id)
    return JSONResponse(content=result, status_code=200)

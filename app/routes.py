from fastapi import APIRouter
from sdx_base.errors.errors import DataError
from starlette.responses import JSONResponse, PlainTextResponse

from app import get_logger
from app.controllers.submission import submission_to_pck, submission_to_spp
from app.definitions.output import PCK, JSON
from app.definitions.spec import Template
from app.definitions.input import SurveyMetadata, Identifier, PrepopData
from app.controllers.prepop import get_prepop

logger = get_logger()
router = APIRouter()


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

    result: PCK = submission_to_pck(data, metadata)
    return PlainTextResponse(content=result, status_code=200)


@router.post("/spp")
async def process_spp(survey_id: str,
                      period_id: str,
                      ru_ref: str,
                      form_type: str,
                      period_start_date: str,
                      period_end_date: str,
                      data_version: str,
                      data: dict) -> PlainTextResponse:
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
    result: JSON = submission_to_spp(data, metadata)
    return PlainTextResponse(content=result, status_code=200, media_type="application/json")


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

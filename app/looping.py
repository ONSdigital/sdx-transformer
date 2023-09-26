import json
from copy import deepcopy

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, PrepopData, Template, Identifier, Field, SurveyMetadata, ListCollector
from app.execute import execute
from app.interpolate import interpolate
from app.populate import populate_mappings


logger = get_logger()

survey_mapping: dict[str, str] = {
    "001": "looping"
}


def get_looping(loop_data: ListCollector, survey_metadata: SurveyMetadata) -> str:
    """
    Performs the steps required to transform looped data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"])
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])



def get_build_spec(survey_id: str) -> BuildSpec:
    """
    Looks up the relevant build spec based on the provided survey id
    """
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/looping/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec

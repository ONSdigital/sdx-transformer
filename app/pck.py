import json

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, Value, PCK, Data, SurveyMetadata
from app.execute import execute
from app.formatters.cora_formatter import CORAFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.interpolate import interpolate
from app.populate import populate_mappings, add_implicit_values

logger = get_logger()

survey_mapping: dict[str, str] = {
    "134": "mwss"
}

formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORAFormatter,
    "COMMON SOFTWARE": CSFormatter,
    "OPEN ROAD": OpenRoadFormatter
}


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"])
    transformed_data: dict[str, Value] = transform(submission_data, build_spec)
    formatter: Formatter = formatter_mapping.get(build_spec["target"])(transformed_data, survey_metadata)
    pck = formatter.generate_pck()
    return pck


def get_build_spec(survey_id: str) -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/pck/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec


def transform(submission_data: Data, build_spec: BuildSpec) -> dict[str, Value]:
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
    full_tree: ParseTree = add_implicit_values(parse_tree)
    populated_tree: ParseTree = populate_mappings(full_tree, submission_data)
    result_data: dict[str, Value] = execute(populated_tree)
    return result_data

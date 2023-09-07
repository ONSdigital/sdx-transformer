import json
import yaml
from os.path import exists

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, Value, PCK, Data, SurveyMetadata
from app.execute import execute
from app.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.interpolate import interpolate
from app.populate import populate_mappings, add_implicit_values

logger = get_logger()

survey_mapping: dict[str, str] = {
    "009": "mbs",
    "017": "stocks",
    "074": "bricks",
    "092": "mes",
    "127": "mcg",
    "134": "mwss",
    "144": "ukis",
    "171": "acas",
    "202": "abs",
}

formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORAFormatter,
    "CORA_MES": MESFormatter,
    "CS": CSFormatter,
    "OpenROAD": OpenRoadFormatter,
}


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"])
    add_metadata_to_input_data(submission_data, survey_metadata)
    transformed_data: dict[str, Value] = transform(submission_data, build_spec)
    f: Formatter.__class__ = formatter_mapping.get(build_spec["target"])
    formatter: Formatter = f(build_spec["period_format"],
                             build_spec["pck_period_format"]
                             if "pck_period_format" in build_spec else build_spec["period_format"],
                             build_spec["form_mapping"]
                             if "form_mapping" in build_spec else {})
    pck = formatter.generate_pck(transformed_data, survey_metadata)
    logger.info("Generated pck file")
    return pck


def get_build_spec(survey_id: str) -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")

    filepath = f"build_specs/pck/{survey_name}.yaml"
    if exists(filepath):
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as y:
            build_spec: BuildSpec = yaml.safe_load(y.read())

    else:
        filepath = f"build_specs/pck/{survey_name}.json"
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as j:
            build_spec: BuildSpec = json.load(j)

    return build_spec


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v


def transform(data: Data, build_spec: BuildSpec) -> dict[str, Value]:
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
    full_tree: ParseTree = add_implicit_values(parse_tree)
    populated_tree: ParseTree = populate_mappings(full_tree, data)
    result_data: dict[str, Value] = execute(populated_tree)
    logger.info("Completed data transformation")
    return result_data

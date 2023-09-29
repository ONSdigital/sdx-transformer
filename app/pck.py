
from sdx_gcp.app import get_logger

from app.build_spec import get_build_spec, get_formatter, interpolate_build_spec
from app.definitions import BuildSpec, ParseTree, Value, PCK, Data, SurveyMetadata
from app.formatters.cora_formatter import CORAFormatter, MESFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.json_formatter import JSONFormatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.transform.execute import execute
from app.transform.interpolate import interpolate
from app.transform.populate import populate_mappings, resolve_value_fields

logger = get_logger()

survey_mapping: dict[str, str] = {
    "009": "mbs",
    "017": "stocks",
    "019": "qcas",
    "024": "fuels",
    "073": "blocks",
    "074": "bricks",
    "092": "mes",
    "127": "mcg",
    "134": "mwss",
    "139": "qbs",
    "144": "ukis",
    "160": "qpses",
    "165": "qpsespb",
    "169": "qpsesrap",
    "171": "acas",
    "182": "vacancies",
    "183": "vacancies",
    "184": "vacancies",
    "185": "vacancies",
    "187": "des",
    "194": "rails",
    "202": "abs",
    "228": "construction",
}

formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORAFormatter,
    "CORA_MES": MESFormatter,
    "CS": CSFormatter,
    "OpenROAD": OpenRoadFormatter,
    "JSON": JSONFormatter,
}


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"], survey_mapping)
    add_metadata_to_input_data(submission_data, survey_metadata)
    transformed_data: dict[str, Value] = transform(submission_data, build_spec)
    formatter = get_formatter(build_spec, formatter_mapping)
    pck = formatter.generate_pck(transformed_data, survey_metadata)
    logger.info("Generated pck file")
    return pck


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v


def transform(data: Data, build_spec: BuildSpec) -> dict[str, Value]:
    full_tree: ParseTree = interpolate_build_spec(build_spec)
    populated_tree: ParseTree = populate_mappings(full_tree, data)
    result_data: dict[str, Value] = execute(populated_tree)
    logger.info("Completed data transformation")
    return result_data

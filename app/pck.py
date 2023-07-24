import json

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import Submission, BuildSpec, ParseTree, Value, SubmissionJson, PCK
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


def get_pck(submission_json: SubmissionJson) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission.
    """
    submission: Submission = to_submission(submission_json)
    build_spec: BuildSpec = get_build_spec(submission)
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
    full_tree: ParseTree = add_implicit_values(parse_tree)
    populated_tree: ParseTree = populate_mappings(full_tree, submission["data"])
    result_data: dict[str, Value] = execute(populated_tree)
    formatter: Formatter = formatter_mapping.get(build_spec["target"])(result_data, submission["metadata"])
    pck = formatter.generate_pck()
    return pck


def to_submission(submission_json: dict[str, dict[str, str] | str]) -> Submission:
    """
    Extracts the 'useful' parts of the submission json to create a Submission instance.
    """
    submission: Submission = {
        "tx_id": str(submission_json["tx_id"]),
        "metadata": {
            "survey_id": submission_json["survey_metadata"]["survey_id"],
            "period_id": submission_json["survey_metadata"]["period_id"],
            "ru_ref": submission_json["survey_metadata"]["ru_ref"],
            "form_type": submission_json["survey_metadata"]["form_type"],
        },
        "data": {k: str(v) for k, v in submission_json["data"].items()}
    }
    return submission


def get_build_spec(submission: Submission) -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    survey_id = submission["metadata"]["survey_id"]
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/pck/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec

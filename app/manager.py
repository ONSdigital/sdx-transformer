import json
import os
from io import BytesIO

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import Submission, BuildSpec, ParseTree, Value
from app.execute import execute
from app.formatters.cora_formatter import CORAFormatter
from app.formatters.cs_formatter import CSFormatter
from app.formatters.formatter import Formatter
from app.formatters.open_road_formatter import OpenRoadFormatter
from app.in_memory_zip import InMemoryZip
from app.interpolate import interpolate


logger = get_logger()

survey_mapping: dict[str, str] = {
    "134": "mwss"
}

formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORAFormatter,
    "COMMON SOFTWARE": CSFormatter,
    "OPEN ROAD": OpenRoadFormatter
}


def transform(submission_json: dict[str, dict[str, str] | str]) -> BytesIO:
    submission: Submission = to_submission(submission_json)
    build_spec: BuildSpec = get_build_spec(submission)

    pck_name, pck = get_pck(submission, build_spec)

    receipt = ""
    receipt_name = ""

    image = ""
    image_name = ""

    json_file = ""
    json_name = ""

    zip_file = InMemoryZip()
    return zip_file.append(os.path.join("EDC_QData", pck_name), pck) \
        .append(os.path.join("EDC_QReceipts", receipt_name), receipt) \
        .append(os.path.join("EDC_QImages", "Images", image_name), image) \
        .append(os.path.join("EDC_QJson", json_name), json_file) \
        .get()


def get_pck(submission: Submission, build_spec: BuildSpec) -> tuple[str, str]:
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"], submission["data"])
    result_data: dict[str, Value] = execute(parse_tree)
    formatter: Formatter = formatter_mapping.get(build_spec["target"])(result_data, submission["metadata"])

    pck = formatter.get_pck()
    pck_name = formatter.pck_name(submission["tx_id"])

    return pck_name, pck


def to_submission(submission_json: dict[str, dict[str, str] | str]) -> Submission:
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
    survey_id = submission["metadata"]["survey_id"]
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec

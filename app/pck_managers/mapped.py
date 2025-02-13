
from sdx_gcp.app import get_logger

from app.build_specs.build_spec import PckSpecReader
from app.config.formatters import formatter_mapping
from app.config.specs import build_spec_mapping
from app.definitions import ParseTree, Value, PCK, Data, SurveyMetadata
from app.transform.execute import execute
from app.transform.populate import populate_mappings

logger = get_logger()


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    build_spec_reader: PckSpecReader = PckSpecReader(survey_metadata, build_spec_mapping, formatter_mapping)
    add_metadata_to_input_data(submission_data, survey_metadata)
    transformed_data: dict[str, Value] = transform(submission_data, build_spec_reader.interpolate())
    formatter = build_spec_reader.get_formatter()
    pck = formatter.generate_pck(transformed_data, survey_metadata)
    logger.info("Generated pck file")
    return pck


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v


def transform(data: Data, parse_tree: ParseTree) -> dict[str, Value]:
    populated_tree: ParseTree = populate_mappings(parse_tree, data)
    result_data: dict[str, Value] = execute(populated_tree)
    logger.info("Completed data transformation")
    return result_data

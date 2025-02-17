
from sdx_gcp.app import get_logger

from app.config.dependencies import get_flat_transformer, get_build_spec_mapping, get_executor, get_func_lookup, \
    get_spec_repository, get_formatter_mapping
from app.definitions.spec import ParseTree
from app.definitions.data import Data, SurveyMetadata, PCK, Value
from app.definitions.transformer import TransformerBase


logger = get_logger()


def get_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    transformer: TransformerBase = get_flat_transformer(
        survey_metadata,
        get_build_spec_mapping(get_spec_repository()),
        get_executor(get_func_lookup()),
        get_formatter_mapping(),
    )

    add_metadata_to_input_data(submission_data, survey_metadata)
    tree: ParseTree = transformer.interpolate()
    transformed_data: dict[str, Value] = transformer.run(tree, submission_data)
    logger.info("Completed data transformation")
    formatter = transformer.get_formatter()
    pck = formatter.generate_pck(transformed_data, survey_metadata)
    logger.info("Generated pck file")
    return pck


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v

from app import get_logger
from app.config.dependencies import get_flat_transformer, get_build_spec_mapping, get_executor, get_func_lookup, \
    get_spec_repository, get_formatter_mapping, get_spp_spec_mapping
from app.definitions.spec import ParseTree, BuildSpec
from app.definitions.input import Data, SurveyMetadata, Value
from app.definitions.output import PCK, JSON
from app.definitions.transformer import TransformerBase


logger = get_logger()


def flat_to_pck(submission_data: Data, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to generate a pck file from the submission data.
    """
    transformer: TransformerBase = get_flat_transformer(
        survey_metadata,
        get_build_spec_mapping(get_spec_repository()),
        get_executor(get_func_lookup()),
        get_formatter_mapping(),
    )

    pck: PCK = _run(submission_data, survey_metadata, transformer)
    logger.info("Generated pck file")
    return pck


def flat_to_spp(submission_data: Data, survey_metadata: SurveyMetadata) -> JSON:
    transformer: TransformerBase = get_flat_transformer(
        survey_metadata,
        get_spp_spec_mapping(get_spec_repository()),
        get_executor(get_func_lookup()),
        get_formatter_mapping(),
    )

    json_str: JSON = _run(submission_data, survey_metadata, transformer)
    logger.info("Generated spp file")
    return json_str


def _run(submission_data: Data, survey_metadata: SurveyMetadata, transformer: TransformerBase) -> str:
    spec: BuildSpec = transformer.get_spec()
    if spec.get("default_template", False):
        tree: ParseTree = {qcode: f'#{qcode}' for qcode in submission_data.keys()}
    else:
        add_metadata_to_input_data(submission_data, survey_metadata)
        tree: ParseTree = transformer.interpolate()

    transformed_data: dict[str, Value] = transformer.run(tree, submission_data)
    logger.info("Completed data transformation")
    formatter = transformer.get_formatter()
    return formatter.generate_pck(transformed_data, survey_metadata)


def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v

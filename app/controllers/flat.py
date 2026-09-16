from sdx_base.errors.errors import DataError

from app import get_logger
from app.config.dependencies import get_flat_transformer, get_build_spec_mapping, get_executor, get_func_lookup, \
    get_spec_repository, get_formatter_mapping, get_spp_spec_mapping
from app.definitions.spec import ParseTree, BuildSpec
from app.definitions.input import Data, SurveyMetadata, Value, LoopedData
from app.definitions.output import PCK, JSON
from app.definitions.transformer import TransformerBase
from app.services.formatters.looping_formatter import LoopingFormatter
from app.transformers.looped import LoopedSpecTransformer

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


def _get_looping(looped_data: LoopedData, survey_metadata: SurveyMetadata, transformer: LoopedSpecTransformer) -> PCK:
    """
    Performs the steps required to transform looped data.
    """
    try:
        data_section: Data = looped_data['data_section']

        # CS can only handle one instance. Therefore, convert all looped data back into 'regular' data
        if transformer.get_spec()["target"] == "CS":
            looped_sections: dict[str, dict[str, Data]] = looped_data["looped_sections"]
            item_dict: dict[str, Data]
            for item_dict in looped_sections.values():
                data: Data
                for data in item_dict.values():
                    data_section.update(data)

            looped_data["looped_sections"] = {}

        full_tree: ParseTree = transformer.interpolate()
        transformed_data_section: dict[str, Value] = transformer.run(full_tree, data_section)
        result_data = {k: v for k, v in transformed_data_section.items() if v is not Empty}

        formatter: LoopingFormatter = transformer.get_formatter()
        formatter.set_original(list_data)

        looped_sections: dict[str, dict[str, Data]] = looped_data['looped_sections']
        if looped_sections:
            looped_tree: ParseTree = transformer.interpolate_looped()

            for data_dict in looped_sections.values():
                instance_id = 1
                for list_item_id, d in data_dict.items():
                    transformed_data: dict[str, Value] = transformer.run(looped_tree, d)
                    # remove any values that are empty or already appear in the data section
                    result = {k: v for k, v in transformed_data.items() if v is not Empty}
                    formatter.create_or_update_instance(instance_id=str(instance_id), data=result,
                                                        list_item_id=list_item_id)
                    instance_id += 1

        return formatter.generate_pck(result_data, survey_metadata)

    except KeyError as ke:
        logger.error(f'Missing required key!: {str(ke)}')
        raise DataError(ke)

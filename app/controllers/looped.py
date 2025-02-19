from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.services.berd.berd_transformer import berd_to_spp
from app.config.dependencies import get_looped_transformer, get_build_spec_mapping, get_spec_repository, get_executor, \
    get_func_lookup, get_formatter_mapping
from app.definitions.input import Data, SurveyMetadata, AnswerCode, ListCollector, LoopedData, Empty, Value
from app.definitions.output import PCK
from app.definitions.spec import ParseTree
from app.services.formatters.looping_formatter import LoopingFormatter
from app.transformers.looped import LoopedSpecTransformer

logger = get_logger()


def get_looping(list_data: ListCollector, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to transform looped data.
    """
    try:

        # temporary solution for Berd --------------
        if survey_metadata["survey_id"] == "002" and survey_metadata["form_type"] == "0001":
            return berd_to_spp(list_data, survey_metadata)
        # ------------------------------------------

        transformer: LoopedSpecTransformer = get_looped_transformer(
            survey_metadata,
            get_build_spec_mapping(get_spec_repository()),
            get_executor(get_func_lookup()),
            get_formatter_mapping(),
        )
        looped_data: LoopedData = convert_to_looped_data(list_data)
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


def set_data_value(d: Data, qcode: str, value: str):
    """
    Setter function to enforce string type
    for value
    """
    d[qcode] = str(value)


def get_answer_code(answer_id: str, data: ListCollector) -> AnswerCode:
    """
    Given an answer id, find the first matching answer code
    associated with this answer_id
    """
    for ac in data['answer_codes']:
        if ac['answer_id'] == answer_id:
            return ac


def get_qcode(answer_id: str, answer_value: str, data: ListCollector) -> str:
    """
    Used to find the qcode for answers_codes that have an answer_value field, this
    is usually for answers that have multiple values, such as a checkbox
    """
    for ac in data['answer_codes']:
        if ac['answer_id'] == answer_id:
            if 'answer_value' not in ac or answer_value == ac['answer_value']:
                return ac['code']


def find_data(data: ListCollector, list_item_id=None) -> Data:
    """
    This function will get the data associated with a specific list_item_id (if specified)
    otherwise it will get the data of all NON looping answers (those without a list_item_id)
    """

    # Store our Data object
    data_section = {}

    for answer in data['answers']:

        # This allows the function to handle data with or without list_item_id's and only process the relevant answers
        if ("list_item_id" not in answer.keys() and not list_item_id) or (
                "list_item_id" in answer.keys() and answer['list_item_id'] == list_item_id):

            # Fetch the answer code for the current answer_id
            ac = get_answer_code(answer['answer_id'], data)
            answer_value = answer['value']

            # If the value is a list, lookup each value in the answer_codes section of the ListCollector
            if isinstance(answer_value, list):

                # Create a mapping of list value to qcode.
                # Sometimes the values don't have unique qcodes, where this is the case append instead.
                list_value_mapping: dict[str, str] = {}
                for v in answer_value:
                    qcode: str = get_qcode(answer['answer_id'], v, data)
                    if qcode in list_value_mapping:
                        list_value_mapping[qcode] = f'{list_value_mapping[qcode]}\n{v}'
                    else:
                        list_value_mapping[qcode] = v

                # Add the mappings to the data
                for qcode, v in list_value_mapping.items():
                    set_data_value(data_section, qcode, v)

            # If the value is a dict, we suffix the qcode with a counter value
            # So if the qcode is 7, each item in the dict becomes 7.1, 7.2 etc
            elif isinstance(answer_value, dict):
                i = 0
                for value in answer_value.values():
                    i += 1
                    set_data_value(data_section, f"{ac['code']}.{i}", value)

            # Else, we have a simple 1-1 mapping
            else:
                set_data_value(data_section, ac['code'], answer_value)

    return data_section


def convert_to_looped_data(data: ListCollector) -> LoopedData:
    """
    Entry point for creating our loopedData object, we take in data
    as a ListCollector, create each section of the loopData
    """

    # ----- Step 1. Create our looped sections -----

    # Find the 'lists' section in the data, then assign each list.name to an empty list
    looped_sections: dict[str, dict[str, Data]] = {d['name']: {} for d in data['lists']}

    for group in data['lists']:

        # Fetch the group name (i.e. people, pets etc)
        name: str = group['name']

        for list_item_id in group['items']:
            # Fetch the data associated with this list_item_id and store
            d: Data = find_data(data, list_item_id)

            looped_sections[name][list_item_id] = d

    # ----- Step 2. Create the data section part of the loopedData -----
    data_section = find_data(data)

    return {
        "looped_sections": looped_sections,
        "data_section": data_section
    }

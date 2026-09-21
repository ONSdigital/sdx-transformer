from typing import Final

from sdx_base.errors.errors import DataError

from app import get_logger
from app.services.berd.berd_transformer import berd_to_spp
from app.config.dependencies import get_looped_transformer, get_build_spec_mapping, get_spec_repository, get_executor, \
    get_func_lookup, get_formatter_mapping, get_spp_spec_mapping
from app.definitions.input import Data, SurveyMetadata, AnswerCode, ListCollector, LoopedData, Empty, Value, Group
from app.definitions.output import PCK, JSON
from app.definitions.spec import ParseTree

from app.services.formatters.formatter import Formatter
from app.transformers.looped import LoopedSpecTransformer

logger = get_logger()


def submission_to_pck(submission_data: dict, survey_metadata: SurveyMetadata) -> PCK:
   return process_submission(submission_data, survey_metadata, spp=False)


def submission_to_spp(submission_data: dict, survey_metadata: SurveyMetadata) -> JSON:
   return process_submission(submission_data, survey_metadata, spp=True)


def process_submission(submission_data: dict, survey_metadata: SurveyMetadata, spp: bool) -> PCK:
    transformer: LoopedSpecTransformer = get_looped_transformer(
        survey_metadata,
        get_spp_spec_mapping(get_spec_repository()) if spp else get_build_spec_mapping(get_spec_repository()),
        get_executor(get_func_lookup()),
        get_formatter_mapping(),
    )

    default = transformer.is_default()

    looped_data: LoopedData
    groups: list[Group] = []

    data_version: str = survey_metadata["data_version"] if "data_version" in survey_metadata else "0.0.1"
    if data_version == "0.0.3":
        list_data: ListCollector = submission_data
        if list_data is None:
            raise DataError("Submission data is not in json format")

        if survey_metadata["survey_id"] == "002" and survey_metadata["form_type"] == "0001":
            return berd_to_spp(list_data, survey_metadata)

        looped_data = convert_to_looped_data(list_data)
        groups = list_data.get("lists", [])

    else:
        looped_data = {
            "data_section": submission_data,
            "looped_sections": {}
        }
    return _get_looping(looped_data, groups, survey_metadata, transformer, default)


def _get_looping(looped_data: LoopedData,
                 groups: list[Group],
                 survey_metadata: SurveyMetadata,
                 transformer: LoopedSpecTransformer,
                 default: bool = False) -> PCK:
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

        if default:
            full_tree: ParseTree = {qcode: f'#{qcode}' for qcode in data_section.keys()}
        else:
            full_tree: ParseTree = transformer.interpolate()
            add_metadata_to_input_data(data_section, survey_metadata)

        transformed_data_section: dict[str, Value] = transformer.run(full_tree, data_section)
        result_data = {k: v for k, v in transformed_data_section.items() if v is not Empty}

        formatter: Formatter = transformer.get_formatter(survey_metadata)
        formatter.add_data("0", result_data)

        looped_sections: dict[str, dict[str, Data]] = looped_data['looped_sections']
        instance_counter = 1
        i = 1
        if looped_sections:
            looped_tree: ParseTree = transformer.interpolate_looped()

            for data_dict in looped_sections.values():
                for list_item_id, d in data_dict.items():
                    transformed_data: dict[str, Value] = transformer.run(looped_tree, d)
                    # remove any values that are empty or already appear in the data section
                    result = {k: v for k, v in transformed_data.items() if v is not Empty}

                    instance_id, i = get_instance_id(list_item_id, groups, i)
                    if instance_id == "":
                        instance_id = str(instance_counter)
                        instance_counter += 1

                    formatter.add_data(instance_id, data=result)

        return formatter.create_output()

    except KeyError as ke:
        logger.error(f'Missing required key!: {str(ke)}')
        raise DataError(ke)


# supplementary_data_mappings: list[dict[str, str]]
DEFAULT_REF: Final[str] = "N0000000"


def get_instance_id(list_item_id: str, groups: list[Group], i: int) -> tuple[str, int]:
    for group in groups:
        if group["name"] == "additional_sites_name":
            return f"N{str(i).zfill(len(DEFAULT_REF)-1)}", i + 1
        else:
            supplementary_data_mappings = group.get("supplementary_data_mappings", [])
            for mapping in supplementary_data_mappings:
                for k, v in mapping.items():
                    if v == list_item_id:
                        return mapping["identifier"], i
    return "", i


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

def add_metadata_to_input_data(submission_data: Data, survey_metadata: SurveyMetadata):
    for k, v in survey_metadata.items():
        submission_data[k] = v

import json

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, SurveyMetadata, \
    ListCollector, LoopedData, Data, AnswerCode
from app.interpolate import interpolate

logger = get_logger()

survey_mapping: dict[str, str] = {
    "001": "looping"
}


def get_looping(loop_data: ListCollector, survey_metadata: SurveyMetadata) -> str:
    """
    Performs the steps required to transform looped data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"])
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])


def get_build_spec(survey_id: str) -> BuildSpec:
    """
    Looks up the relevant build spec based on the provided survey id
    """
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/looping/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec


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
        if ac['answer_id'] == answer_id and answer_value == ac['answer_value']:
            return ac['code']


def my_new_func(data: ListCollector, list_item_id=None) -> Data:
    """
    This function will get the data associated with a specific list_item_id (if specified)
    otherwise it will get the data of all NON looping answers (those without a list_item_id)
    """

    # Store our Data object
    data_section = {}

    for answer in data['answers']:

        # This allows the function to handle data with or without list_item_id's and only process the relevant answers
        if ("list_item_id" not in answer.keys() and not list_item_id) or ("list_item_id" in answer.keys() and answer['list_item_id'] == list_item_id):

            # Fetch the answer code for the current answer_id
            ac = get_answer_code(answer['answer_id'], data)
            answer_value = answer['value']

            # If the value is a list, lookup each value in the answer_codes section of the ListCollector
            if isinstance(answer_value, list):

                for v in answer_value:
                    qcode: str = get_qcode(answer['answer_id'], v, data)
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
    looped_sections: dict[str, list[Data]] = {d['name']: [] for d in data['lists']}

    for group in data['lists']:

        # Fetch the group name (i.e. people, pets etc)
        name: str = group['name']

        for list_item_id in group['items']:

            # Fetch the data associated with this list_item_id and store
            d: Data = my_new_func(data, list_item_id)

            looped_sections[name].append(d)

    # ----- Step 2. Create the data section part of the loopedData -----
    data_section = my_new_func(data)

    return {
        "looped_sections": looped_sections,
        "data_section": data_section
    }


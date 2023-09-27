import json
from os.path import exists

import yaml
from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, SurveyMetadata, \
    ListCollector, LoopedData, Data, AnswerCode, Value, BuildSpecError, PCK
from app.execute import execute
from app.formatters.cora_looping_formatter import CORALoopingFormatter
from app.formatters.formatter import Formatter
from app.formatters.looping_formatter import LoopingFormatter
from app.interpolate import interpolate
from app.populate import resolve_value_fields, populate_mappings

logger = get_logger()

survey_mapping: dict[str, str] = {
    "001": "looping"
}

formatter_mapping: dict[str, Formatter.__class__] = {
    "CORA": CORALoopingFormatter,
}


def get_formatter(build_spec: BuildSpec) -> LoopingFormatter:
    f: LoopingFormatter.__class__ = formatter_mapping.get(build_spec["target"])
    if f is None:
        raise BuildSpecError(f"Unable to find formatter for target: {build_spec['target']}")

    period_format = build_spec["period_format"]
    pck_period_format = build_spec["pck_period_format"] if "pck_period_format" in build_spec else period_format
    form_mapping = build_spec["form_mapping"] if "form_mapping" in build_spec else {}

    formatter: LoopingFormatter = f(build_spec["period_format"], pck_period_format, form_mapping)
    return formatter


def get_looping(list_data: ListCollector, survey_metadata: SurveyMetadata) -> PCK:
    """
    Performs the steps required to transform looped data.
    """
    build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"])
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
    full_tree: parse_tree = resolve_value_fields(parse_tree)
    looped_data: LoopedData = convert_to_looped_data(list_data)

    data_section: Data = looped_data['data_section']
    populated_tree: parse_tree = populate_mappings(full_tree, data_section)
    result_data: dict[str, Value] = execute(populated_tree)

    formatter: LoopingFormatter = get_formatter(build_spec)

    looped_sections: dict[str, list[Data]] = looped_data['looped_sections']
    for data_list in looped_sections.values():
        instance_id = 1
        for d in data_list:
            populated_tree: parse_tree = populate_mappings(full_tree, d)
            result: dict[str, Value] = execute(populated_tree)
            formatter.create_or_update_instance(instance_id=str(instance_id), data=result)
            instance_id += 1

    return formatter.generate_pck(result_data, survey_metadata)


def get_build_spec(survey_id: str) -> BuildSpec:
    """
    Looks up the relevant build spec for the submission provided.
    """
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")

    filepath = f"build_specs/looping/{survey_name}.yaml"
    if exists(filepath):
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as y:
            build_spec: BuildSpec = yaml.safe_load(y.read())

    else:
        filepath = f"build_specs/looping/{survey_name}.json"
        logger.info(f"Getting build spec from {filepath}")
        with open(filepath) as j:
            build_spec: BuildSpec = json.load(j)

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
            d: Data = find_data(data, list_item_id)

            looped_sections[name].append(d)

    # ----- Step 2. Create the data section part of the loopedData -----
    data_section = find_data(data)

    return {
        "looped_sections": looped_sections,
        "data_section": data_section
    }

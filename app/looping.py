import json
from copy import deepcopy

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, PrepopData, Template, Identifier, Field, SurveyMetadata, \
    ListCollector, LoopedData, Data, Answer, AnswerCode
from app.execute import execute
from app.interpolate import interpolate
from app.populate import populate_mappings


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


def get_answer_code(answer_id: str, data: ListCollector) -> AnswerCode:
    for ac in data['answer_codes']:
        if ac['answer_id'] == answer_id:
            return ac


def get_qcode(answer_id: str, answer_value: str, data: ListCollector) -> str:
    for ac in data['answer_codes']:
        if ac['answer_id'] == answer_id and answer_value == ac['answer_value']:
            return ac['code']


def get_list_item_data(list_item_id: str, data: ListCollector) -> Data:

    d = {}

    for answer in data['answers']:
        if "list_item_id" in answer.keys() and answer['list_item_id'] == list_item_id:
            ac = get_answer_code(answer['answer_id'], data)

            answer_value = answer['value']

            # If the value is a list, lookup each value
            if isinstance(answer_value, list):

                for v in answer_value:
                    qcode: str = get_qcode(answer['answer_id'], v, data)
                    d[qcode] = v
            elif isinstance(answer_value, dict):
                i = 0
                for value in answer_value.values():
                    i += 1
                    d[f"{ac['code']}.{i}"] = value
            else:
                d[ac['code']] = answer_value

    return d


def convert_to_looped_data(data: ListCollector) -> LoopedData:

    # Create our looped sections
    looped_sections: dict[str, list[Data]] = {d['name']: [] for d in data['lists']}

    for group in data['lists']:

        name: str = group['name']

        for list_item_id in group['items']:
            d: Data = get_list_item_data(list_item_id, data)
            looped_sections[name].append(d)

    # Create the data part of the loopedData
    data_section = {}

    for answer in data['answers']:
        if "list_item_id" not in answer.keys():
            ac = get_answer_code(answer['answer_id'], data)

            answer_value = answer['value']

            # If the value is a list, lookup each value
            if isinstance(answer_value, list):

                for v in answer_value:
                    qcode: str = get_qcode(answer['answer_id'], v, data)
                    data_section[qcode] = v
            elif isinstance(answer_value, dict):
                i = 0
                for value in answer_value.values():
                    i += 1
                    data_section[f"{ac['code']}.{i}"] = value
            else:
                data_section[ac['code']] = answer_value

    return {
        "looped_sections": looped_sections,
        "data_section": data_section
    }


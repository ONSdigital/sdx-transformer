from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.berd.berd_transformer import berd_to_spp, berd_to_image
from app.build_spec import get_build_spec, get_formatter, interpolate_build_spec
from app.definitions import BuildSpec, ParseTree, SurveyMetadata, \
    ListCollector, LoopedData, Data, AnswerCode, Value, PCK, Empty
from app.formatters.cora_looping_formatter import CORALoopingFormatter
from app.formatters.image_looping_formatter import ImageLoopingFormatter
from app.formatters.looping_formatter import LoopingFormatter
from app.formatters.spp_looping_formatter import SPPLoopingFormatter
from app.transform.execute import execute
from app.transform.populate import populate_mappings

logger = get_logger()

survey_mapping: dict[str, str] = {
    "001": "looping",
    "068": "qrt",
    "999": "looping-spp",
}

formatter_mapping: dict[str, LoopingFormatter.__class__] = {
    "CORA": CORALoopingFormatter,
    "SPP": SPPLoopingFormatter,
    "Image": ImageLoopingFormatter,
}


def get_looping(list_data: ListCollector, survey_metadata: SurveyMetadata, use_image_formatter: bool = False) -> PCK:
    """
    Performs the steps required to transform looped data.
    """
    try:

        # temporary solution for Berd --------------
        if survey_metadata["survey_id"] == "002" and survey_metadata["form_type"] == "0001":
            if use_image_formatter:
                return berd_to_image(list_data, survey_metadata)
            else:
                return berd_to_spp(list_data, survey_metadata)
        # ------------------------------------------

        build_spec: BuildSpec = get_build_spec(survey_metadata["survey_id"], survey_mapping, "looping")

        full_tree: ParseTree = interpolate_build_spec(build_spec)
        looped_data: LoopedData = convert_to_looped_data(list_data)

        data_section: Data = looped_data['data_section']
        populated_tree: ParseTree = populate_mappings(full_tree, data_section)
        transformed_data_section: dict[str, Value] = execute(populated_tree)
        result_data = {k: v for k, v in transformed_data_section.items() if v is not Empty}

        if use_image_formatter:
            # reset the target in the build spec
            bs: BuildSpec = build_spec.copy()
            bs["target"] = "Image"
            formatter: LoopingFormatter = get_formatter(bs, formatter_mapping)
        else:
            formatter: LoopingFormatter = get_formatter(build_spec, formatter_mapping)

        formatter.set_original(list_data)

        looped_sections: dict[str, dict[str, Data]] = looped_data['looped_sections']

        for data_dict in looped_sections.values():
            instance_id = 1
            for list_item_id, d in data_dict.items():
                populated_tree: ParseTree = populate_mappings(full_tree, d)
                transformed_data: dict[str, Value] = execute(populated_tree)
                result = {k: v for k, v in transformed_data.items() if v is not Empty}
                formatter.create_or_update_instance(instance_id=str(instance_id), data=result, list_item_id=list_item_id)
                instance_id += 1

        return formatter.generate_pck(result_data, survey_metadata)

    except KeyError as ke:
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

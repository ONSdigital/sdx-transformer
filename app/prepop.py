import json
from copy import deepcopy

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.definitions import BuildSpec, ParseTree, PrepopData, Template, Identifier, Field
from app.execute import execute
from app.interpolate import interpolate
from app.populate import populate_mappings

logger = get_logger()

survey_mapping: dict[str, str] = {
    "068": "tiles"
}


def get_prepop(survey_id: str, prepop_data: PrepopData) -> dict[Identifier: Template]:
    build_spec: BuildSpec = get_build_spec(survey_id)
    parse_tree: ParseTree = interpolate(build_spec["template"], build_spec["transforms"])
    result: dict[Identifier: Template] = {}
    for ru_ref, data_list in prepop_data.items():
        items: list[Template] = []
        for data in data_list:
            populated_tree: ParseTree = populate_mappings(parse_tree, data)
            result_item: Template = execute(populated_tree)
            items.append(result_item)

        item = merge_items(items, build_spec["item_list_path"])
        result[ru_ref] = item

    return result


def get_build_spec(survey_id: str) -> BuildSpec:
    survey_name = survey_mapping.get(survey_id)
    if survey_name is None:
        raise DataError(f"Could not lookup survey id {survey_id}")
    filepath = f"build_specs/prepop/{survey_name}.json"
    logger.info(f"Getting build spec from {filepath}")
    with open(filepath) as f:
        build_spec: BuildSpec = json.load(f)

    return build_spec


def merge_items(items: list[Template], item_list_path: str) -> Template:
    first_item = deepcopy(items[0])
    item_list = get_item_list(first_item, item_list_path)
    for i in range(1, len(items)):
        item_list.append(get_item_list(items[i], item_list_path)[0])

    return first_item


def get_item_list(template: Template, item_list_path: str) -> list[Field]:
    path: list[str] = item_list_path.split(".")
    t = template
    for p in path:
        if p not in t:
            raise DataError(f'Incorrect item_list_path: {item_list_path}')
        t = t[p]

    if not isinstance(t, list):
        raise DataError(f'Incorrect item_list_path: {item_list_path}')

    return t

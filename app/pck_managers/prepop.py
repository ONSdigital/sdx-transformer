from copy import deepcopy

from sdx_gcp.app import get_logger
from sdx_gcp.errors import DataError

from app.build_spec import get_build_spec, interpolate_build_spec
from app.definitions import BuildSpec, ParseTree, PrepopData, Template, Identifier, Field
from app.transform.clean import clean
from app.transform.execute import execute
from app.transform.populate import populate_mappings

logger = get_logger()

survey_mapping: dict[str, str] = {
    "066": "land",
    "068": "tiles",
    "071": "slate",
    "076": "marine",
    "221": "bres",
    "241": "brs",
}


def get_prepop(prepop_data: PrepopData, survey_id: str) -> dict[Identifier: Template]:
    """
    Performs the steps required to transform prepopulated data.
    """
    build_spec: BuildSpec = get_build_spec(survey_id, survey_mapping, "prepop")
    parse_tree: ParseTree = interpolate_build_spec(build_spec)

    result: dict[Identifier: Template] = {}
    for ru_ref, data_list in prepop_data.items():
        items: list[Template] = []
        for data in data_list:
            populated_tree: ParseTree = populate_mappings(parse_tree, data)
            result_item: Template = execute(populated_tree)
            result_item = clean(result_item)
            items.append(result_item)

        item = merge_items(items, build_spec["item_list_path"])
        result[ru_ref] = item

    logger.info("Completed prepop data transformation")
    return result


def merge_items(items: list[Template], item_list_path: str) -> Template:
    """
    Multiple items can exist for one identifier.
    These are merged into one template so that each identifier
    is represented by one (and only one) template.
    """
    first_item = deepcopy(items[0])
    item_list = get_item_list(first_item, item_list_path)
    for i in range(1, len(items)):
        item_list.append(get_item_list(items[i], item_list_path)[0])

    return first_item


def get_item_list(template: Template, item_list_path: str) -> list[Field]:
    """
    Find the location within the template of the item sub list.
    """
    path: list[str] = item_list_path.split(".")
    t = template
    for p in path:
        if p not in t:
            raise DataError(f'Incorrect item_list_path: {item_list_path}')
        t = t[p]

    if not isinstance(t, list):
        raise DataError(f'Incorrect item_list_path: {item_list_path}')

    return t

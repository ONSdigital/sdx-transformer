from copy import deepcopy
from typing import Optional

from sdx_base.errors.errors import DataError

from app import get_logger
from app.config.dependencies import get_prepop_transformer, get_prepop_spec_mapping, get_spec_repository, get_executor, \
    get_func_lookup, get_formatter_mapping
from app.definitions.spec import BuildSpec, ParseTree, Template
from app.definitions.input import Identifier, PrepopData, Field
from app.definitions.transformer import TransformerBase
from app.services.transform.clean import clean

logger = get_logger()


def get_prepop(prepop_data: PrepopData, survey_id: str) -> dict[Identifier: Template]:
    """
    Performs the steps required to transform prepopulated data.
    """
    transformer: TransformerBase = get_prepop_transformer(
        survey_id,
        get_prepop_spec_mapping(get_spec_repository()),
        get_executor(get_func_lookup()),
        get_formatter_mapping(),
    )

    build_spec: BuildSpec = transformer.get_spec()
    parse_tree: ParseTree = transformer.interpolate()

    result: dict[Identifier: Template] = {}

    if not isinstance(prepop_data, dict):
        raise DataError("Prepop data is not in correct format")

    for ru_ref, data_list in prepop_data.items():
        items: list[Template] = []
        for data in data_list:
            result_item: Template = transformer.run(parse_tree, data)
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
    Templates that do not contain the local unit path are removed.
    """
    first_item = deepcopy(items[0])
    item_list = get_item_list(first_item, item_list_path)
    for i in range(1, len(items)):
        item = get_item_list(items[i], item_list_path)
        if item:
            item_list.append(item[0])

    return first_item


def get_item_list(template: Template, item_list_path: str) -> Optional[list[Field]]:
    """
    Find the location within the template of the item sub list.

    If not found return None
    """
    path: list[str] = item_list_path.split(".")
    t = template
    for p in path:
        if p not in t:
            logger.warn(f'Incorrect item_list_path: {item_list_path}')
            return None
        t = t[p]

    if not isinstance(t, list):
        logger.warn(f'Incorrect item_list_path: {item_list_path}')
        return None

    return t

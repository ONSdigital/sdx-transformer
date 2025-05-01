from typing import final

from app.definitions.spec import Template
from app.definitions.input import Empty, Field
from app.services.transform.tree_walker import TreeWalker

BLACK_LIST: final = ["", Empty, [], {}]
DICT_BLACK_LIST: final = [Empty, [], {}]


class CleanTreeWalker(TreeWalker):
    """
    Removing blank and empty fields from the Template
    - Items with a blank or empty value will be removed
    - Parents with ALL empty children will be removed
    """

    def on_dict(self, name: str, field: dict[str, Field]) -> Field:
        found: bool = False
        for v in super().on_dict(name, field).values():
            if v not in BLACK_LIST:
                found = True
        if not found:
            # remove dicts with no values not in the blacklist
            return {}
        return {k: v for k, v in super().on_dict(name, field).items() if v not in DICT_BLACK_LIST}

    def on_list(self, name: str, field: list[Field]) -> Field:
        return [f for f in [self.evaluate_field(name, i) for i in field] if f not in BLACK_LIST]


def clean(template: Template) -> Template:
    # This comprehension is needed at the top level as the TreeWalker cannot handle top level items
    return {k: v for k, v in CleanTreeWalker(template).walk_tree().items() if v not in BLACK_LIST}

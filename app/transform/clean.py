from typing import final

from app.definitions import Template, Field, Empty
from app.transform.tree_walker import TreeWalker

BLACK_LIST: final = ["", Empty, [], {}]


class CleanTreeWalker(TreeWalker):

    def on_dict(self, name: str, field: dict[str, Field]) -> Field:
        return {k: v for k, v in super().on_dict(name, field).items() if v not in BLACK_LIST}

    def on_list(self, name: str, field: list[Field]) -> Field:
        return [f for f in [self.evaluate_field(name, i) for i in field] if f not in BLACK_LIST]


def clean(template: Template) -> Template:
    return {k: v for k, v in CleanTreeWalker(template).walk_tree().items() if v not in BLACK_LIST}

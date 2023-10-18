from typing import final

from app.definitions import Template, Field, Empty
from app.transform.tree_walker import TreeWalker

BLACK_LIST: final = ["", Empty, [], {}]


class CleanTreeWalker(TreeWalker):

    def on_dict(self, name: str, field: dict[str, Field]) -> Field:
        d = super().on_dict(name, field)
        return {k: v for k, v in d.items() if v not in BLACK_LIST}

    def on_list(self, name: str, field: list[Field]) -> Field:
        new_list = []
        for item in field:
            f = self.evaluate_field(name, item)
            if f not in BLACK_LIST:
                new_list.append(f)
        return new_list


def clean(template: Template) -> Template:
    tree: Template = CleanTreeWalker(template).walk_tree()
    return {k: v for k, v in tree.items() if v not in BLACK_LIST}

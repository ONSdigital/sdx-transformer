from typing import final

from app.definitions import Template, Field, Empty
from app.transform.tree_walker import TreeWalker

BLACK_LIST: final = ["", Empty, []]


class CleanTreeWalker(TreeWalker):

    def on_list(self, name: str, field: list[Field]) -> Field:
        new_list = []
        for item in field:
            f = self.evaluate_field(name, item)
            if f not in BLACK_LIST:
                new_list.append(f)
        return new_list


def clean(template: Template) -> Template:

    return CleanTreeWalker(template).walk_tree()

    # result_template = {}
    # for key, value in template.items():
    #
    #     if isinstance(value, list):
    #
    #
    # return result_template


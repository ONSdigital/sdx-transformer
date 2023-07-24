from collections.abc import Callable
from typing import Self

from app.definitions import ParseTree, Field


class TreeWalker:

    def __init__(
            self, tree: ParseTree,
            on_str: Callable[[str, str, Self], Field] = lambda name, field, walker: field):

        self._tree = tree
        self._on_str = on_str

    def on_list(self, name: str, field: list[Field], walker: Self) -> Field:
        return [self.evaluate_field(name, item) for item in field]

    def on_dict(self, name: str, field: dict[str, Field], walker: Self) -> Field:
        return {k: self.evaluate_field(k, v) for k, v in field.items()}

    def evaluate_field(self, name: str, field: Field) -> Field:
        if isinstance(field, dict):
            return self.on_dict(name, field, self)
        elif isinstance(field, list):
            return self.on_list(name, field, self)
        elif isinstance(field, str):
            return self._on_str(name, field, self)
        return field

    def walk_tree(self) -> ParseTree:
        result: ParseTree = {}
        for name, field in self._tree.items():
            result[name] = self.evaluate_field(name, field)

        return result

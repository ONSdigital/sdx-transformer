from collections.abc import Callable
from typing import Self

from app.definitions import ParseTree, Field


class TreeWalker:
    """
    Creates a new ParseTree by walking the provided ParseTree and
    performing the given function whenever a leaf node is reached.
    A function simply returning the leaf node is provided by default.

    Subclasses can override the existing functions for encountering
    each type of node. These each have access to the encountered
    fields' name and value, and the tree walker through the self parameter
    - allowing for full customization of the resulting tree.
    """
    def __init__(
            self, tree: ParseTree,
            on_str: Callable[[str, str, Self], Field] = lambda name, field, walker: field):

        self._tree = tree
        self._current = tree
        self._on_str = on_str

    def on_list(self, name: str, field: list[Field]) -> Field:
        return [self.evaluate_field(name, item) for item in field]

    def on_dict(self, name: str, field: dict[str, Field]) -> Field:
        return {k: self.evaluate_field(k, v) for k, v in field.items()}

    def evaluate_field(self, name: str, field: Field) -> Field:
        if isinstance(field, dict):
            return self.on_dict(name, field)
        elif isinstance(field, list):
            return self.on_list(name, field)
        elif isinstance(field, str):
            return self._on_str(name, field, self)
        return field

    def walk_tree(self) -> ParseTree:
        result: ParseTree = {}
        self._current = result
        for name, field in self._tree.items():
            result[name] = self.evaluate_field(name, field)

        return result

    def read_from_current(self, name: str) -> str:
        return self._current.get(name)

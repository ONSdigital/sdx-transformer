from copy import deepcopy
from typing import Final

from app.definitions import ParseTree, Field, Data
from app.tree_walker import TreeWalker


MAPPING_PREFIX: Final = "#"


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    """
    Create a "value" field (in args) for all transforms in the tree
    without an explicit value. The value is assumed to be a mapping
    to the root key for which the transform is a leaf node of. E.g:
        {
            "123": {
                name: ROUND
                args: {
                    nearest: 10
                }
            }
        }

    Will become:
        {
            "123": {
                name: ROUND
                args: {
                    nearest: 10,
                    value: "#123"
                }
            }
        }

    Transforms that already contain a value field (even if it is the empty string)
    will remain untouched.
    """

    class ValueTreeWalker(TreeWalker):

        def __init__(self, tree: ParseTree, qcode: str):
            super().__init__(tree)
            self._qcode = qcode

        def on_dict(self, name: str, field: dict[str, Field], walker: TreeWalker) -> Field:
            if name == "args":
                if "value" not in field:
                    f = deepcopy(field)
                    f["value"] = f'{MAPPING_PREFIX}{self._qcode}'
                    return super().on_dict(name, f, self)

            return super().on_dict(name, field, self)

    result_tree = deepcopy(parse_tree)

    for k, v in result_tree.items():
        if isinstance(v, dict):
            result_tree[k] = ValueTreeWalker(tree=v, qcode=k).walk_tree()
        else:
            result_tree[k] = v

    return result_tree


def populate_mappings(parse_tree: ParseTree, data: Data) -> ParseTree:
    """
    Use the provided data to populate the tree.

    E.g. The tree:
        {
            "123": {
                name: ROUND
                args: {
                    nearest: 10,
                    value: "#123"
                }
            }
        }

    will become:

        {
            "123": {
                name: ROUND
                args: {
                    nearest: 10,
                    value: "450"
                }
            }
        }

    for the data:
        {
            "123": "450",
            "124": "42"
        }
    """
    def base_str(_name: str, field: str, _walker: TreeWalker) -> Field:
        if field.startswith(MAPPING_PREFIX):
            return data.get(field[1:])
        return field

    return TreeWalker(tree=parse_tree, on_str=base_str).walk_tree()
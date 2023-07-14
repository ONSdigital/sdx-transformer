from copy import deepcopy
from typing import Final

from app.definitions import Template, Transforms, Transform, ParseTree, Data, Field
from app.tree_walker import TreeWalker

FUNCTION_PREFIX: Final = "$"
MAPPING_PREFIX: Final = "#"


def interpolate(template: Template, transforms: Transforms, data: Data) -> ParseTree:
    nested_transforms = expand_nested_transforms(transforms)
    parse_tree = map_template(template, nested_transforms)
    inverted_parse_tree = invert_post_transforms(parse_tree)
    full_tree = add_implicit_values(inverted_parse_tree)
    mapped_tree = interpolate_mappings(full_tree, data)
    return mapped_tree


def expand_nested_transforms(transforms: Transforms) -> Transforms:
    def on_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(FUNCTION_PREFIX):
            return walker.evaluate_field(name, transforms.get(field))
        return field

    return TreeWalker(tree=transforms, on_str=on_str).walk_tree()


def map_template(template: Template, transforms: Transforms) -> ParseTree:
    result: ParseTree = {}

    for k, v in template.items():
        if v.startswith(FUNCTION_PREFIX):
            t: Transform = transforms[v]
            result[k] = t
        else:
            result[k] = v
    return result


def invert_post_transforms(tree: ParseTree) -> ParseTree:
    class PostTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if "post" in field:
                child = deepcopy(field)
                parent = deepcopy(field["post"])
                child.pop("post")
                parent["args"]["value"] = child
                return self.on_dict(name, parent)

            return super().on_dict(name, field)

    return PostTreeWalker(tree=tree).walk_tree()


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:

    class ValueTreeWalker(TreeWalker):

        def __init__(self, tree: ParseTree, qcode: str):
            super().__init__(tree)
            self._qcode = qcode

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if name == "args":
                if "value" not in field:
                    f = deepcopy(field)
                    f["value"] = f'{MAPPING_PREFIX}{self._qcode}'
                    return super().on_dict(name, f)

            return super().on_dict(name, field)

    result_tree = deepcopy(parse_tree)

    for k, v in result_tree.items():
        if isinstance(v, dict):
            result_tree[k] = ValueTreeWalker(tree=v, qcode=k).walk_tree()
        else:
            result_tree[k] = v

    return result_tree


def interpolate_mappings(parse_tree: ParseTree, data: Data) -> ParseTree:
    def base_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(MAPPING_PREFIX):
            return data.get(field[1:])
        return field

    return TreeWalker(tree=parse_tree, on_str=base_str).walk_tree()

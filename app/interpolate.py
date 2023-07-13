from copy import deepcopy
from typing import Final

from app.definitions import Template, Transforms, Transform, ParseTree, Data, Field
from app.tree_walker import TreeWalker

FUNCTION_PREFIX: Final = "$"
MAPPING_PREFIX: Final = "#"


def interpolate(template: Template, transforms: Transforms, data: Data) -> ParseTree:
    nested_transforms = interpolate_nested_functions(transforms)
    parse_tree = map_template(template, nested_transforms)
    inverted_parse_tree = invert_post_functions(parse_tree)
    full_tree = add_implicit_values(inverted_parse_tree)
    mapped_tree = interpolate_mappings(full_tree, data)
    return mapped_tree


def interpolate_nested_functions(transforms: Transforms) -> Transforms:
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


def invert_post_functions(tree: ParseTree) -> ParseTree:
    class PostTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if "post" in field:
                root = deepcopy(field)
                parent = deepcopy(field["post"])
                root.pop("post")
                parent["args"]["value"] = root
                return self.on_dict(name, parent)

            return super().on_dict(name, field)

    return PostTreeWalker(tree=tree).walk_tree()


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    tree = deepcopy(parse_tree)
    for k, v in tree.items():

        class ValueTreeWalker(TreeWalker):

            def on_dict(self, name: str, field: dict[str, Field]) -> Field:
                if name == "args":
                    if "value" not in field:
                        f = deepcopy(field)
                        f["value"] = f'{MAPPING_PREFIX}{k}'
                        return super().on_dict(name, f)

                return super().on_dict(name, field)

        if isinstance(v, dict):
            tree[k] = ValueTreeWalker(tree=v).walk_tree()
        else:
            tree[k] = v

    return tree


def interpolate_mappings(parse_tree: ParseTree, data: Data) -> ParseTree:
    def base_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(MAPPING_PREFIX):
            return data.get(field[1:])
        return field

    return TreeWalker(tree=parse_tree, on_str=base_str).walk_tree()

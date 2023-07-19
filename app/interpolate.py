from copy import deepcopy
from typing import Final

from app.definitions import Template, Transforms, ParseTree, Field
from app.tree_walker import TreeWalker

FUNCTION_PREFIX: Final = "$"


def interpolate(template: Template, transforms: Transforms) -> ParseTree:
    nested_transforms = expand_nested_transforms(transforms)
    parse_tree = map_template(template, nested_transforms)
    inverted_parse_tree = invert_post_transforms(parse_tree)
    return inverted_parse_tree


def expand_nested_transforms(transforms: Transforms) -> Transforms:
    def on_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(FUNCTION_PREFIX):
            return walker.evaluate_field(name, transforms.get(field))
        return field

    return TreeWalker(tree=transforms, on_str=on_str).walk_tree()


def map_template(template: Template, transforms: Transforms) -> ParseTree:

    def on_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(FUNCTION_PREFIX):
            return walker.evaluate_field(name, transforms.get(field))
        return field

    return TreeWalker(tree=template, on_str=on_str).walk_tree()


def invert_post_transforms(tree: ParseTree) -> ParseTree:
    class PostTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field], walker: TreeWalker) -> Field:
            if "post" in field:
                child = deepcopy(field)
                parent = deepcopy(field["post"])
                child.pop("post")
                parent["args"]["value"] = child
                return self.on_dict(name, parent, self)

            return super().on_dict(name, field, self)

    return PostTreeWalker(tree=tree).walk_tree()

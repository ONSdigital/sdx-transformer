from copy import deepcopy
from typing import Final

from app import get_logger
from app.definitions.spec import Template, Transforms, ParseTree, BuildSpecError
from app.definitions.input import Field
from app.services.transform.tree_walker import TreeWalker

logger = get_logger()


TRANSFORM_PREFIX: Final[str] = "$"


def interpolate(template: Template, transforms: Transforms) -> ParseTree:
    """
    Returns a ParseTree in the structure of the template,
    with all the transforms interpolated.

    This includes expanding all nested transforms that exist
    within the args, and inverting all 'post' transforms e.g:

        "DIVIDE": {
            "name": "DIVIDE",
            "args": {
                "value": "$MULTIPLY",
            },
            post: "$ROUND
        },

    The above snippet will result in a ParseTree such that ROUND has a value field of DIVIDE,
    within which will have a value field of MULTIPLY.
    """
    nested_transforms = expand_nested_transforms(transforms)
    parse_tree = map_template(template, nested_transforms)
    inverted_parse_tree = invert_post_transforms(parse_tree)
    return inverted_parse_tree


def expand_nested_transforms(transforms: Transforms) -> Transforms:
    """
    Fully expand each transform i.e. where ever a transform is referenced,
    replace the reference with the full definition. Note that transforms
    can reference other transforms prior to the referenced transform
    being expanded.
    """
    def on_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(TRANSFORM_PREFIX):
            nested = transforms.get(field[1:])
            if nested is None:
                raise BuildSpecError(f"Nested transform {field} not found!")
            return walker.evaluate_field(name, nested)
        return field

    return TreeWalker(tree=transforms, on_str=on_str).walk_tree()


def map_template(template: Template, transforms: Transforms) -> ParseTree:
    """
    Create a ParseTree in the structure of the template
    """
    def on_str(name: str, field: str, walker: TreeWalker) -> Field:
        if field.startswith(TRANSFORM_PREFIX):
            root = transforms.get(field[1:])
            if root is None:
                raise BuildSpecError(f"Root transform {field} not found!")
            return walker.evaluate_field(name, root)
        return field

    return TreeWalker(tree=template, on_str=on_str).walk_tree()


def invert_post_transforms(tree: ParseTree) -> ParseTree:
    """
    Invert all transforms that are held in the "post" field in another transform.
    E.g. if A contains B in its post field then B will become the parent of A in the tree,
    and contain A in its value field (in the args field).
    """
    class PostTreeWalker(TreeWalker):

        def on_dict(self, name: str, field: dict[str, Field]) -> Field:
            if "post" in field:
                child = deepcopy(field)
                parent = deepcopy(field["post"])
                child.pop("post")
                if "value" in parent["args"]:
                    # Overwriting an existing value might be intended if the parent is used
                    # in multiple places. Therefore, provide a warning but do not raise an exception.
                    logger.warning(f"Overwriting value {parent['args']['value']} with child!")
                parent["args"]["value"] = child
                return self.on_dict(name, parent)

            return super().on_dict(name, field)

    return PostTreeWalker(tree=tree).walk_tree()

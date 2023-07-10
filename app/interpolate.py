from typing import Final

from app.definitions import Template, Transforms, Transform, ParseTree, Data

FUNCTION_PREFIX: Final = "$"
MAPPING_PREFIX: Final = "#"


def interpolate_functions(template: Template, transforms: Transforms) -> ParseTree:
    result: dict[str, Transform | str] = {}

    for k, v in template.items():
        if v.startswith(FUNCTION_PREFIX):
            t: Transform = transforms[v]
            root = get_root(t, transforms)
            result[k] = root
        else:
            result[k] = v
    return result


def get_root(t: Transform, transforms: Transforms) -> Transform:
    root = t.copy()
    if "post" in t:
        parent = transforms[t["post"]]
        root.pop("post")
        parent["args"]["value"] = root
        root = get_root(parent, transforms)
    return root


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    tree = parse_tree.copy()
    for k, v in tree.items():
        if not isinstance(v, dict):
            continue

        t: Transform = v
        while "value" in t["args"]:
            t = t["args"]["value"]

        t["args"]["value"] = f"#{k}"

    return tree


def interpolate_mappings(parse_tree: ParseTree, data: Data) -> ParseTree:
    tree = parse_tree.copy()

    for k, v in tree.items():
        if v.startswith(MAPPING_PREFIX):
            tree[k] = data[v[1:]]

    return tree


from app.definitions import Template, Transforms, Transform, ParseTree

FUNCTION_PREFIX = "$"


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
    root = t
    if "post" in t:
        parent = transforms[t["post"]]
        t.pop("post")
        parent["args"]["value"] = t
        root = get_root(parent, transforms)
    return root


def add_implicit_values(parse_tree: ParseTree) -> ParseTree:
    pass
